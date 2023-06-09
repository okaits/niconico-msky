#!/usr/bin/env python3
"""
Generate twitter-like sharing URL of nicovideo videos for Misskey
"""

import webbrowser

import config
import get_videodata
import share_url

def main():
    """ Main """
    print("niconico-msky v1.0.0")
    print()
    config_data = config.check_config()

    # Loop
    while True:
        print()
        # Ask for videoid
        print("Enter your video id.")
        print("Enter \"exit\" to quit.")
        videoid = input("videoid> ")
        if videoid == "exit":
            break

        # Get video's metadata
        try:
            videodata = get_videodata.get_videodata(videoid)
        except get_videodata.Error.FetchFailed:
            print("Wrong video id or no internet connection. Please try it again.")
            continue
        print("Video informations:")
        print(f"\tTitle\t\t: {videodata.title}")
        print(f"\tURL\t\t: {videodata.url}")
        print(f"\tContributer\t: {videodata.username} ({videodata.userid})")
        prompt = input("Is it OK? (Y/n)> ")
        if prompt == "n" or prompt == "N" :
            print("Aborted.")
            continue

        # Generate URL
        text = share_url.ShareURL.gen_text(videodata)
        url = share_url.ShareURL.gen_url(config_data.serverurl, text)

        # Output generated URL
        print(f"Generated URL: {url}")

        # Ask for using browser
        browserprompt = input("Do you want to open it with your default browser? (Y/n)> ")
        if not ( browserprompt == "n" or browserprompt == "N" ):
            print("Opening browser...")
            try:
                webbrowser.open_new_tab(url)
            except webbrowser.Error:
                print("Something went wrong with your browser.")

if __name__ == "__main__":
    main()
