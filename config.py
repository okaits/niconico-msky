""" Config module """
import json
import os

class Config():
    """ Config class """
    def __init__(self) -> None:
        self.servers: list[dict] = []

    def to_json(self) -> str:
        """ Convert to JSON """
        return json.dumps({"servers": self.servers})

    def save(self, converted_json: str = None):
        """ Save config file """
        if not converted_json:
            converted_json = self.to_json()
        with open(os.path.dirname(__file__) + "/config.json", "w", encoding="utf-8") as configfile:
            configfile.write(converted_json)
        print("Saved.")

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

def update_config(no_add: bool = False, delete: bool = False, serverurl: str = None) -> None:
    """ Initial config wizard """

    if delete:
        # Deleting server requested
        try:
            config = check_config(auto_creating=False)
        except Config.Error.CouldNotReadConfigFile:
            # Config file corrupted
            print("Config file corrupted. Aborting. (use -c to re-generate)")
            return
        if len(config.servers) > 1 and not serverurl:
            # Server choosing
            print("Multiple servers found in your config file:")
            count = 0
            for serverurl in config.servers:
                print(f"{count}: {serverurl}")
                count = count + 1
            choice = input("Which server do you want to delete? > ")
            try:
                serverurl = config.servers[int(choice)]
            except KeyError:
                print("Value not valid.")
                return
        elif len(config.servers) == 1 and not serverurl:
            # Skip server choosing
            serverurl = config.servers[0]
        # Remove server
        try:
            config.servers.remove(serverurl)
        except ValueError:
            print("URL not valid.")
            return
        # Save
        config.save()

    elif os.path.exists(os.path.dirname(__file__) + "/config.json") and not no_add:
        # Config file exists
        try:
            # Read current config file
            config = check_config(auto_creating=False)
        except Config.Error.CouldNotReadConfigFile:
            # Config file corrupted
            print("Config file corrupted. creating new one.")
            update_config(no_add=True)
            return
        # Ask user for server URL, then remove scheme and /
        serverurl = input("Misskey server> ").lstrip("https://").lstrip("http://") \
            if not serverurl else serverurl
        if serverurl.endswith("/"):
            serverurl = serverurl[:1]
        # Prevent duplication
        if serverurl in config.servers:
            print("Same entry found in your config file. Aborting.")
            return
        # Save
        config.servers.append(serverurl)
        config.save()

    else:
        # Config file doesn't exists or regenerating requested
        # Ask user for server URL, then remove scheme and /
        serverurl = input("Misskey server> ").lstrip("https://").lstrip("http://") \
            if not serverurl else serverurl
        # Save
        config = Config()
        config.servers.append(serverurl)
        config.save()
