import pytest
from utils.yaml_utils import clear_yaml


@pytest.fixture(scope='session', autouse=True)
def fixture():
    # 删除新增的用户
    # 删除新增的项目
    # 清空依赖数据
    clear_yaml()
