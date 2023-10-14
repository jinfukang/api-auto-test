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

        res = self.send_request(name, method, base_url, url, **caseinfo['request'])
        # 记录请求耗时 单位：毫秒
        log("请求耗时：%d ms" % (res.elapsed.microseconds / 1000))

        if 'extract' in caseinfo.keys():
            result = res.json()
            if result.get('code') == 200 and "token" in json.dumps(result):
                for item in caseinfo['extract']:
                    for key, value in item.items():
                        id = jsonpath(result, value)[0]
                        write_data({key: id})
        assert_result(caseinfo['validate'], res.json())

    def replace_value(self, data):
        if '${' in data:
            start_index = data.index('${') + 2
            end_index = data.index('}')
            func_name = data[start_index:end_index].split('(')[0]
            param = data[start_index:end_index].split('(')[1].split(')')[0]
            if param != '':
                if ',' in param:
                    args = param.split(",")
                    return getattr(self.obj, func_name)(*args)
                else:
                    return getattr(self.obj, func_name)(param)
            else:
                return getattr(self.obj, func_name)()

    def send_request(self, name, method, baseurl, url, **kwargs):
        log("------接口测试开始啦------")
        try:
            baseurl = self.replace_value(baseurl)
            log("用例名称：%s" % name)
            log("请求路径：%s" % baseurl + url)
            log("请求方法：%s" % method)
            return self.session.request(url=baseurl + url, method=method, **kwargs)

        except Exception as e:
            print(str(e))
