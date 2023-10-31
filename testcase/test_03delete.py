import pytest
from debugTalk.debug_talk import DebugTalk
from utils.parameterize_util import read_testcase_yaml
from utils.request_util import RequestUtils


class TestDelete:
    """
    delete接口测试
    """
    @pytest.mark.parametrize("testcase", read_testcase_yaml("data/user/delete.yaml"))
    def test_delete_user(self, testcase):
        RequestUtils(DebugTalk()).standard_yaml(testcase)

    @pytest.mark.parametrize("testcase", read_testcase_yaml("data/project/delete.yaml"))
    def test_delete_project(self, testcase):
        RequestUtils(DebugTalk()).standard_yaml(testcase)