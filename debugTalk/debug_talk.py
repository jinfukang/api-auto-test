import yaml, random, string
from utils.yaml_utils import get_root_path


class DebugTalk:

    @staticmethod
    def read_config_yaml(one_node=None, two_node=None):
        with open(get_root_path() + "/config.yaml", mode="r", encoding="utf-8") as file:
            return yaml.full_load(file)[one_node][two_node]

    @staticmethod
    def read_config_yaml_by_key(one_node):
        with open(get_root_path() + "/config.yaml", mode="r", encoding="utf-8") as file:
            return yaml.full_load(file)[one_node]

    @staticmethod
    def read_extract_yaml(one_node=None):
        with open(get_root_path() + "/extract.yaml", mode="r", encoding="utf-8") as file:
            return yaml.full_load(file)[one_node]

    @staticmethod
    def get_random_username():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(20))
