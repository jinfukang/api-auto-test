import pytest
from utils.parameterize_util import read_testcase_yaml
from utils.request_util import RequestUtils
from debugTalk.debug_talk import DebugTalk

class TestProject:
    @pytest.mark.parametrize("testcase", read_testcase_yaml('data/project/add.yaml'))
    def test_add(self, testcase):
        RequestUtils(DebugTalk()).standard_yaml(testcase)


if __name__ == '__main__':
    pytest.main(["-s", "test_project.py"])