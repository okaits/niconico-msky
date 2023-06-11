#!/usr/bin/env python3
"""
Generate twitter-like sharing URL of nicovideo videos for Misskey
"""

import webbrowser
from argparse import ArgumentParser as ap
from argparse import Namespace as argparse_Namespace

import config
import get_videodata
import share_url

def argument_parsing() -> argparse_Namespace:
    """ ArgumentParser """
    parser = ap(
        prog="niconico-msky",
        description="Generate twitter-like sharing URL of nicovideo videos for misskey."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("-v", "--videoid", help="Video ID", metavar="ID", default=None)
    mode.add_argument("-i", "--interactive", help="Interactive Mode", action="store_true", default=False)
    mode.add_argument("-c", "--configure", help="Create config file, or append new server", action="store_true", default=False)
    parser.add_argument("-u", "--server_url", help="Server URL", default=None)
    return parser.parse_args()

def main_process(videoid: str, url: str, interactive: bool = True) -> None:
    """ Main process. (Get videodata, generate URL, and open it) """
    # Get video's metadata
    try:
        videodata = get_videodata.get_videodata(videoid)
    except get_videodata.Error.FetchFailed:
        print("Wrong video id or no internet connection. Please try it again.")
        return
    if interactive is True:
        print(get_videodata.gen_video_info(videodata))
        prompt = input("Is it OK? (Y/n)> ")
        if prompt == "n" or prompt == "N" :
            print("Aborted.")
            return

    # Generate URL
    text = share_url.ShareURL.gen_text(videodata)
    url = share_url.ShareURL.gen_url(url, text)

    # Output generated URL
    if interactive is True:
        print(f"Generated URL: {url}")
    else:
        print(url)

    # Ask for using browser
    if interactive is True:
        browserprompt = input("Do you want to open it with your default browser? (Y/n)> ")
        if not ( browserprompt == "n" or browserprompt == "N" ):
            print("Opening browser...")
            try:
                webbrowser.open_new_tab(url)
            except webbrowser.Error:
                print("Something went wrong with your browser.")

def main() -> None:
    """ Main """

    # Argument parsing
    args = argument_parsing()

    if args.interactive: # videoid exists in commandline args
        print("niconico-msky v1.0.0\n")

        config_data = config.check_config(auto_creating=True) if not args.server_url else None
        if len(config_data.servers) > 1 if config_data else True and not args.server_url:
            print("Multiple servers found in your config file:")
            count = 0
            for serverurl in config_data.servers:
                print(f"{count}: {serverurl}")
                count = count + 1
            choice = input("Which server do you want to use? > ")
            try:
                serverurl = config_data.servers[int(choice)]
            except KeyError:
                print("Value not valid.")
                return
        else:
            serverurl = config_data.servers[0] if not args.server_url else args.server_url

        while True:
            # Ask for videoid
            print("Enter your video id.")
            print("Enter \"exit\" to quit.")
            videoid = input("videoid> ")
            if videoid == "exit":
                break

            main_process(videoid, serverurl)
            print()
    elif args.configure:
        print("niconico-msky v1.1.0\n")
        config.update_config(serverurl=args.server_url)
    else:
        try:
            config_data = config.check_config(auto_creating=False)
        except config.Config.Error.CouldNotReadConfigFile:
            print("Couldn't read config file. "
            "Config file may be corrupt or non-existent.")
            return
        if len(config_data.servers) > 1 and not args.server_url:
            for serverurl in config_data.servers:
                main_process(args.videoid, serverurl, interactive=False)
        else:
            main_process(
                args.videoid,
                config_data.servers[0] if not args.server_url else args.server_url,
                interactive=False
            )


if __name__ == "__main__":
    main()
