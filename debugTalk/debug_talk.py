import yaml, random, string
from utils.yaml_util import get_root_path
from utils.mysql_util import DBUtil
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

    @staticmethod
    def get_random_phone():
        area_code = ["13", "14", "15", "16", "17", "18", "19"]  # 手机号码前缀
        middle_number = str(random.randint(0, 999)).zfill(3)
        last_number = str(random.randint(0, 9999)).zfill(4)
        phone_number = random.choice(area_code) + middle_number + last_number
        return phone_number
    
    @staticmethod
    def fetch_one(sql):
        """
        执行sql语句
        :param sql:
        :return:
        """
        with DBUtil() as db:
            return db.execute(sql)