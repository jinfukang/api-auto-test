from utils.logger_util import log


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
        assert all_flag == 0
        log("接口测试成功")
    except Exception as e:
        log("接口测试失败")
        log("断言异常：%s" % str(e))
        raise e
    finally:
        log("------接口测试结束------\n")


def equal_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        log("预期结果：%s" % expect)
        log("实际结果：%s" % real)
        if key == "code":
            if value != real['code']:
                flag += 1
        if key == "msg":
            if value != real['msg']:
                flag += 1
    return flag


# 包含
def contains_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        if key == "message":
            if value not in real['message']:
                flag += 1
    return flag


# 大于
def greater_assert(expect, real):
    flag = 0
    for key, value in expect.items():
        if key == "code":
            if value > real['code']:
                flag += 1
    return flag
