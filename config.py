""" Config module """
import json
import os

class Config():
    """ Config class """
    def __init__(self) -> None:
        self.servers: list[dict] = ""

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
                servers = config["servers"]
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
    config.servers = servers
    return config

def update_config(no_add: bool = False, serverurl: str = None) -> None:
    """ Initial config wizard """

    if os.path.exists(os.path.dirname(__file__) + "/config.json") and not no_add:
        # Config file exists
        try:
            # Read current config file
            config = check_config(auto_creating=False)
        except Config.Error.CouldNotReadConfigFile:
            # Config file corrupted
            print("Config file corrupted. creating new one.")
            update_config(no_add=True)
            return
        serverurl = input("Misskey server> ") if not serverurl else serverurl
        if serverurl.endswith("/"):
            serverurl = serverurl[:1]
        # Append new server to config
        config = {"servers": config.servers}
        config["servers"].append(serverurl)
    else:
        # Config file doesn't exists or regenerating requested
        serverurl = input("Misskey server> ") if not serverurl else serverurl
        if serverurl.endswith("/"):
            serverurl = serverurl[:1]
        config = {"servers": [serverurl]}

    # Save config file
    configjson = json.dumps(config)
    with open(os.path.dirname(__file__) + "/config.json", "w", encoding="utf-8") as configfile:
        configfile.write(configjson)
    print("Config file saved.")
