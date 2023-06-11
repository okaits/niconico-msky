""" Config module """
import json
import os

class Config():
    """ Config class """
    def __init__(self) -> None:
        self.serverurl: str = ""

    class Error(Exception):
        """ Errors """
        class CouldNotReadConfigFile(Exception):
            """ Couldn't read config file. """

def check_config(auto_creating: bool = True) -> Config:
    """ Check config, then return config """
    while True:
        try:
            with open("config.json", "r", encoding="utf-8") as configfile:
                config = json.load(configfile)
                serverurl = config["serverurl"]
        except (KeyError, FileNotFoundError) as exc:
            if auto_creating is True:
                auto_creating()
            else:
                raise Config.Error.CouldNotReadConfigFile(
                    "Config file corrupted or not found."
                ) from exc
        else:
            break
    config = Config()
    config.serverurl = serverurl
    return config

def create_config() -> None:
    """ Initial config wizard """
    print("Starting initial config wizard...")
    serverurl = input("Misskey server> ")
    if serverurl.endswith("/"):
        serverurl = serverurl[:1]
    config = {"serverurl": serverurl}
    with open(os.path.dirname(__file__) + "/config.json", "w", encoding="utf-8") as configfile:
        configjson = json.dumps(config)
        configfile.write(configjson)
    print("Config file saved.")
