""" Get videodata module """

from typing import Union

import urllib.request
import urllib.error
import xmltodict #pylint: disable=E0401

API_URL = "https://ext.nicovideo.jp/api/getthumbinfo/{videoid}"

class Error(Exception):
    """ Errors """
    class FetchFailed(Exception):
        """ Failed to fetch videodata from API """

class VideoData():
    """ videodata """
    def __init__(self, videoid: str) -> None:
        self.videoid: str = videoid #pylint: disable=C0103
        self.title: str = ""
        self.url: str = ""
        self.username: str = ""
        self.userid: Union[str, int] = ""

def get_videodata(videoid: str) -> VideoData:
    """ Get videodata from nicovideo API, then return VideoData object """
    try:
        with urllib.request.urlopen(API_URL.format(videoid=videoid)) as res:
            response = res.read()
        responsedata = xmltodict.parse(response)["nicovideo_thumb_response"]["thumb"]
    except (KeyError, urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise Error.FetchFailed("nicovideo API Error.") from exc
    data = VideoData(videoid)
    data.title = responsedata["title"]
    data.url = responsedata["watch_url"]
    if "user_nickname" in responsedata:
        data.username = responsedata["user_nickname"]
        data.userid = responsedata["user_id"]
    else:
        data.username = responsedata["ch_name"]
        data.userid = responsedata["ch_id"]
    return data

def gen_video_info(videodata: VideoData) -> str:
    """ Generate video info """
    info = "Video informations:\n"
    info += f"\tTitle\t\t: {videodata.title}\n"
    info += f"\tURL\t\t: {videodata.url}\n"
    info += f"\tContributer\t: {videodata.username} ({videodata.userid})"
    return info
