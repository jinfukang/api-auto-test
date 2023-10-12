import yaml, os


def get_root_path():
    return os.path.abspath(os.getcwd().split("commons")[0])


def read_data(filepath):
    with open(os.path.join(get_root_path(), filepath), mode="r", encoding="utf-8") as file:
        res = yaml.full_load(file)
        return res


def write_data(data=None):
    with open(get_root_path() + "/extract.yaml", mode="a+", encoding="utf-8") as file:
        yaml.dump(data=data, stream=file)


def clear_yaml():
    with open(get_root_path() + "/extract.yaml", mode="w", encoding="utf-8") as file:
        file.truncate()


def read_config_yaml(one_node, two_node):
    with open(get_root_path() + "/config.yaml", mode="r", encoding="utf-8") as file:
        return yaml.full_load(file)[one_node][two_node]


if __name__ == '__main__':
    print(read_config_yaml("log", "log_name"))
