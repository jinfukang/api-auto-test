import json
import requests
from utils.assert_util import assert_result
from utils.yaml_utils import write_data
from jsonpath import jsonpath
from utils.logger_util import log


class RequestUtils:
    def __init__(self, obj):
        self.session = requests.Session()
        self.obj = obj

    def standard_yaml(self, caseinfo):
        name = caseinfo.get("feature")
        base_url = caseinfo.pop('base_url')
        method = caseinfo['request'].pop('method')
        url = caseinfo['request'].pop('url')
        headers = caseinfo['request'].pop('headers')
        res = self.send_request(name, method, base_url, url, headers, **caseinfo['request'])
        log("请求参数：%s" % caseinfo['request'])
        # 记录请求耗时 单位：毫秒
        log("请求耗时：%d ms" % (res.elapsed.microseconds / 1000))
        result = res.json()
        result['time'] = res.elapsed.microseconds / 1000
        if 'extract' in caseinfo.keys():
            if result.get('code') == 200:
                for item in caseinfo['extract']:
                    for key, value in item.items():
                        try:
                            id = jsonpath(result, value)[0]
                        except TypeError:
                            pass
                        else:
                            write_data({key: id})
        assert_result(caseinfo['validate'], result)

    def replace_value(self, data):
        if isinstance(data, str):
            if '${' in data:
                start_index = data.index('${') + 2
                end_index = data.index('}')
                func_name = data[start_index:end_index].split('(')[0]
                param = data[start_index:end_index].split('(')[1].split(')')[0]
                if param != '':
                    if ',' in param:
                        args = param.split(",")
                        if data.index("${") == 0:
                            # 判断是否整体替换 整体替换的情况是 "${xxx(x)}"
                            return getattr(self.obj, func_name)(*args)
                        else:
                            # 部分替换 情况是： "/v1/user/${read_extract_yaml(id)}"  需保留/v1/user 仅替换${x(x)}部分
                            return self.replace_return(data, getattr(self.obj, func_name)(*args))
                    else:
                        if data.index("${") == 0:
                            return getattr(self.obj, func_name)(param)
                        else:
                            return self.replace_return(data, getattr(self.obj, func_name)(param))
                else:
                    return getattr(self.obj, func_name)()

        if isinstance(data, dict):
            for key, value in data.items():
                if '${' in str(value):
                    data[key] = self.replace_value(value)
            return data

    def send_request(self, name, method, baseurl, url, headers, **kwargs):
        log("------接口测试开始啦------")
        try:
            if "${" in baseurl:
                baseurl = self.replace_value(baseurl)
            if "${" in url:
                url = self.replace_value(url)
            if "${" in json.dumps(headers):
                headers = self.replace_value(headers)
            if "${" in json.dumps(kwargs):
                kwargs = self.replace_value(kwargs)
            log("用例名称：%s" % name)
            log("请求路径：%s" % baseurl + url)
            log("请求方法：%s" % method)
            return self.session.request(url=baseurl + url, method=method, headers=headers, **kwargs)

        except Exception as e:
            print(str(e))

    def replace_return(self, old_data, replace_value):
        start_index = old_data.index("${") + 2
        end_index = old_data.index("}")

        new_data = old_data.replace("${" + old_data[start_index:end_index] + "}", str(replace_value))
        return new_data
