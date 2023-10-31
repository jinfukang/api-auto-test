import pytest, os
from utils.yaml_util import clear_yaml


@pytest.fixture(scope='session', autouse=True)
def fixture():
    # 创建依赖文件
    if not os.path.exists("extract.yaml"):
        os.system("type nul>extract.yaml")
    if not os.path.exists("logs"):
        os.mkdir("logs")
    if not os.path.exists("reports"):
        os.mkdir("reports")
    if not os.path.exists("temps"):
        os.mkdir("temps")
    clear_yaml()
