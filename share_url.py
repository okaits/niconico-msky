""" Share URL module """

import urllib.parse
import get_videodata #pylint: disable=E0401

SHARE_TEXT_TEMPLATE = """\
{videotitle}
{videourl}?ref=misskey

#{videoid}
#ニコニコ動画\
"""

class ShareURL():
    """ ShareURL Class """
    def gen_text(videodata: get_videodata.VideoData) -> None: # pylint: disable=E0213
        """ Generate note text """
        return SHARE_TEXT_TEMPLATE.format(
            videotitle=videodata.title, # pylint: disable=E1101
            videourl=videodata.url,     # pylint: disable=E1101
            videoid=videodata.videoid   # pylint: disable=E1101
        )

    def gen_url(serverurl: str, text: str) -> None: #pylint: disable=E0213
        """ Generate share URL from note text """
        quoted_text = urllib.parse.quote(text, encoding="utf-8")
        return f"https://{serverurl}/share?text={quoted_text}"
