import pymysql
from utils.yaml_util import read_config_yaml


class DBUtil:

    def __init__(self):
        self.conn = pymysql.connect(
            host=read_config_yaml('db', 'host'),
            user=read_config_yaml('db', 'user'),
            password=read_config_yaml('db', 'password'),
            db=read_config_yaml('db', 'db'),
        )
        self.cur = self.conn.cursor()

    def __enter__(self):
        return self.cur

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cur.close()
        self.conn.close()
