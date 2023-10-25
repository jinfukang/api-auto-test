import json
from utils.yaml_utils import read_data


def read_testcase_yaml(yaml_path):
    caseinfo = read_data(yaml_path)

    if 'parameterize' in dict(*caseinfo).keys():
        # 解析参数
        res = ddt(*caseinfo)
        return res
    else:
        return caseinfo


def ddt(caseinfo):
    if 'parameterize' in caseinfo.keys():
        caseinfo_str = json.dumps(caseinfo)
        key_list = caseinfo['parameterize'][0]
        data_list = [x for x in caseinfo['parameterize']]
        length_flag = True
        for data in data_list:
            if len(data) != len(key_list):
                length_flag = False
                break

        new_caseinfo = []
        if length_flag:
            for x in range(1, len(data_list)):
                temp_caseinfo = caseinfo_str
                for y in range(0, len(data_list[x])):
                    if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                        temp_caseinfo = temp_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"', str(data_list[x][y]))
                    else:
                        temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}",
                                                              str(data_list[x][y]))
                new_caseinfo.append(json.loads(temp_caseinfo))
        return new_caseinfo
    else:
        return caseinfo
