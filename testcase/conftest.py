import pytest, os
from utils.yaml_utils import clear_yaml


@pytest.fixture(scope='session', autouse=True)
def fixture():
    # 创建依赖文件
    if not os.path.exists("extract.yaml"):
        os.system("type nul>extract.yaml")
    if not os.path.exists("logs"):
        os.mkdir("logs")
    # 删除新增的用户
    # 删除新增的项目
    # 清空依赖数据
    clear_yaml()
