import re

from jsonpath import jsonpath
from utils.logger_util import log
from utils.mysql_util import DBUtil


def _get_values(real, key):
    if isinstance(key, str) and key.startswith("$"):
        values = jsonpath(real, key)
        if not values:
            return []
        return values
    if key in real:
        return [real[key]]
    return []


def _log_assert_case(assert_type, key, expect, actual_values):
    log("[%s] 断言字段：%s，预期：%s，实际：%s" % (assert_type, key, expect, actual_values))


# 判断断言方式
def assert_result(expect, result_json):
    try:
        all_flag = 0
        for item in expect:
            for key, value in item.items():
                if key == "equals":
                    equals_flag = equal_assert(value, result_json)
                    all_flag = all_flag + equals_flag
                if key == "contains":
                    contains_flag = contains_assert(value, result_json)
                    all_flag = all_flag + contains_flag
                if key == "greater":
                    greater_flag = greater_assert(value, result_json)
                    all_flag = all_flag + greater_flag
                if key == "not_None":
                    not_None_flag = not_None_assert(value, result_json)
                    all_flag = all_flag + not_None_flag
                if key == "gt":
                    gt_flag = gt_assert(value, result_json)
                    all_flag = all_flag + gt_flag
                if key == "ge":
                    ge_flag = ge_assert(value, result_json)
                    all_flag = all_flag + ge_flag
                if key == "lt":
                    lt_flag = lt_assert(value, result_json)
                    all_flag = all_flag + lt_flag
                if key == "le":
                    le_flag = le_assert(value, result_json)
                    all_flag = all_flag + le_flag
                if key == "between":
                    between_flag = between_assert(value, result_json)
                    all_flag = all_flag + between_flag
                if key == "starts_with":
                    starts_with_flag = starts_with_assert(value, result_json)
                    all_flag = all_flag + starts_with_flag
                if key == "ends_with":
                    ends_with_flag = ends_with_assert(value, result_json)
                    all_flag = all_flag + ends_with_flag
                if key == "regex":
                    regex_flag = regex_assert(value, result_json)
                    all_flag = all_flag + regex_flag
                if key == "not_contains":
                    not_contains_flag = not_contains_assert(value, result_json)
                    all_flag = all_flag + not_contains_flag
        assert all_flag == 0
        log("接口测试通过")
    except Exception as e:
        log("接口测试失败")
        log("断言异常：%s" % str(e))
        raise e
    finally:
        log("------接口测试结束------\n")


def equal_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("equals", key, value, values)
        if not values or not any(item == value for item in values):
            flag += 1
    return flag


# 包含
def contains_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("contains", key, value, values)
        if not values or not any(str(value) in str(item) for item in values):
            flag += 1
    return flag


# 大于
def greater_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("greater", key, value, values)
        if not values or not any(item <= value for item in values):
            flag += 1
    return flag


# 不为空
def not_None_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        if key == "sql":
            if not value:
                continue
            log("校验SQL：" + value)
            with DBUtil() as db:
                db.execute(value)
                if db.fetchall() is None:
                    flag += 1
            continue
        values = _get_values(real, key)
        _log_assert_case("not_None", key, "not None", values)
        if not values or any(item is None for item in values):
            flag += 1
    return flag


def gt_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("gt", key, value, values)
        if not values or not any(item > value for item in values):
            flag += 1
    return flag


def ge_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("ge", key, value, values)
        if not values or not any(item >= value for item in values):
            flag += 1
    return flag


def lt_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("lt", key, value, values)
        if not values or not any(item < value for item in values):
            flag += 1
    return flag


def le_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("le", key, value, values)
        if not values or not any(item <= value for item in values):
            flag += 1
    return flag


def between_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        if not isinstance(value, (list, tuple)) or len(value) != 2:
            _log_assert_case("between", key, value, "between 需要 [min,max]")
            flag += 1
            continue
        values = _get_values(real, key)
        _log_assert_case("between", key, value, values)
        if not values or not any(value[0] <= item <= value[1] for item in values):
            flag += 1
    return flag


def starts_with_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("starts_with", key, value, values)
        if not values or not any(str(item).startswith(str(value)) for item in values):
            flag += 1
    return flag


def ends_with_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("ends_with", key, value, values)
        if not values or not any(str(item).endswith(str(value)) for item in values):
            flag += 1
    return flag


def regex_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("regex", key, value, values)
        if not values or not any(re.search(value, str(item)) is not None for item in values):
            flag += 1
    return flag


def not_contains_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        values = _get_values(real, key)
        _log_assert_case("not_contains", key, value, values)
        if not values or not all(str(value) not in str(item) for item in values):
            flag += 1
    return flag
