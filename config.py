""" Config module """
import json
import os

class Config():
    """ Config class """
    def __init__(self):
        self.serverurl = ""

def check_config():
    """ Check config, then return config """
    while True:
        try:
            with open("config.json", "r", encoding="utf-8") as configfile:
                config = json.load(configfile)
                serverurl = config["serverurl"]
        except (KeyError, FileNotFoundError):
            _create_config()
        else:
            break
    config = Config()
    config.serverurl = serverurl
    return config

def _create_config():
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
