#!/usr/bin/env python3
"""
Generate twitter-like sharing URL of nicovideo videos for Misskey
"""

import json
import urllib.parse
import urllib.request

import xmltodict  # pylint: disable=E0401


def main():
    """ Main """
    # Check & Read config file
    try:
        with open("config.json", "r", encoding="utf-8") as configfile:
            config = json.load(configfile)
            serverurl = config["serverurl"]
    except (KeyError, FileNotFoundError):
        print("Config file not exists or corrupted. Creating new one...")
        serverurl = input("Misskey server name> ")
        config = {"serverurl": serverurl}
        with open("config.json", "w", encoding="utf-8") as configfile:
            configjson = json.dumps(config)
            configfile.write(configjson)

    # Ask for video id
    videoid = input("nicovideo Video ID> ")
    # Output URL template
    outputurl = f"{serverurl}/share"

    # Request thumbinfo to nicovideo api
    apiurl = f"https://ext.nicovideo.jp/api/getthumbinfo/{videoid}"
    with urllib.request.urlopen(apiurl) as apiresponse:
        response = apiresponse.read()
    responsedict = xmltodict.parse(response)["nicovideo_thumb_response"]["thumb"]
    # Generate text to note
    videotitle = responsedict["title"]
    videourl = responsedict["watch_url"]
    notecontent = f"{videotitle}\n{videourl}?ref=misskey\n\n#{videoid}\n#ニコニコ動画"
    # Generate sharing URL
    notecontentquoted = urllib.parse.quote(notecontent, encoding="utf-8")
    outputurl += f"?text={notecontentquoted}"
    return outputurl

if __name__ == "__main__":
    print(main())
