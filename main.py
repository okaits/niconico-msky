#!/usr/bin/env python3
"""
Generate twitter-like sharing URL of nicovideo videos for Misskey
"""

import json
import urllib.parse
import urllib.request
import urllib.error
import webbrowser

import xmltodict  # pylint: disable=E0401

def main():
    """ Main """
    print("niconico-msky v0.0.1")
    # Check & Read config file
    try:
        with open("config.json", "r", encoding="utf-8") as configfile:
            config = json.load(configfile)
            serverurl = config["serverurl"]
    except (KeyError, FileNotFoundError):
        print("Config file not exists or corrupted. Creating new one...")
        serverurl = input("Misskey server> ")
        if serverurl.endswith("/"):
            serverurl = serverurl[:1]
        config = {"serverurl": serverurl}
        with open("config.json", "w", encoding="utf-8") as configfile:
            configjson = json.dumps(config)
            configfile.write(configjson)

    # Loop
    while True:
        # Ask for video id
        videoid = input("nicovideo Video ID> ")
        # Output URL template
        outputurl = f"{serverurl}/share"

        # Request thumbinfo to nicovideo api
        apiurl = f"https://ext.nicovideo.jp/api/getthumbinfo/{videoid}"
        try:
            with urllib.request.urlopen(apiurl) as apiresponse:
                response = apiresponse.read()
        except (urllib.error.HTTPError, urllib.error.URLError):
            print("Something went wrong while connecting to the nicovideo API server. "\
                "Please try it again.")
            continue
        # Check if response data valid
        responsedict = xmltodict.parse(response)["nicovideo_thumb_response"]
        if "thumb" in responsedict:
            # Valid data
            print("Got valid video metadata from API.")
            responsedict = responsedict["thumb"]
        else:
            # Invalid data
            print("Got invalid video metadata from API. Please try it again.")
            continue
        # Generate text to note
        videotitle = responsedict["title"]
        videourl = responsedict["watch_url"]
        notecontent = f"{videotitle}\n{videourl}?ref=misskey\n\n#{videoid}\n#ニコニコ動画"
        # Generate sharing URL
        notecontentquoted = urllib.parse.quote(notecontent, encoding="utf-8")
        outputurl += f"?text={notecontentquoted}"
        break
    return outputurl

def openbrowser(url):
    """ Output generated URL, then open it with the default browser. """
    print("Url generated: " + url)
    print("Opening with your browser...")
    try:
        webbrowser.open_new_tab(url)
    except webbrowser.Error:
        print("Something went wrong while opening with your browser.")

if __name__ == "__main__":
    generated_url = main()
    openbrowser(generated_url)
