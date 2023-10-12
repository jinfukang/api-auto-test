import pytest
from utils.parameterize_util import read_testcase_yaml
from utils.request_util import RequestUtils
from debugTalk.debug_talk import DebugTalk


class TestUser:
    @pytest.mark.parametrize("testcase", read_testcase_yaml("data/user/add_user.yaml"))
    @pytest.mark.p1
    def test_add(self, testcase):
        RequestUtils(DebugTalk()).standard_yaml(testcase)

    @pytest.mark.parametrize("testcase", read_testcase_yaml("data/user/login.yaml"))
    @pytest.mark.p1
    def test_login(self, testcase):
        RequestUtils(DebugTalk()).standard_yaml(testcase)


if __name__ == '__main__':
    pytest.main()
