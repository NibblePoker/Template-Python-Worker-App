import json


class Config:
    __config_data: dict

    def __init__(self, config_file_path: str):
        with open(config_file_path, "rb") as f:
            self.__config_data = json.loads(f.read().decode("utf-8"))

    def get_config(self, key: str, default_value):
        if key in self.__config_data.keys():
            return self.__config_data.get(key)
        else:
            return default_value
