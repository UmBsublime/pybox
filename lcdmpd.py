
# -*- coding: utf-8 -*-
"""
Display information from mpd.
Configuration parameters:
    - format : indicator text format
    - hide_when_paused / hide_when_stopped : hide any indicator, if
    - host : mpd host
    - max_width : if text length will be greater - it'll shrink it
    - password : mpd password
    - port : mpd port
Format of result string can contain:
    {state} - current state from STATE_CHARACTERS
    Track information:
    {track}, {artist}, {title}, {time}, {album}, {pos}
    In additional, information about next track also comes in,
    in analogue with current, but with next_ prefix, like {next_title}
Requires:
    - python-mpd2 (NOT python2-mpd2)
    # pip install python-mpd2
@author shadowprince
@license Eclipse Public License
"""

import re
from mpd import MPDClient, CommandError, ConnectionError
from socket import error as SocketError
from time import time


class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 2
    color = 'BLUE'
    format = '{artist}-{title}'
    host = 'localhost'
    max_width = 16
    port = '6600'

    def __init__(self):
        self.text = ''

    def current_track(self, colors):

        self.colors = {'play': 'GREEN',
                  'stop': 'RED'}
        text = ""
        try:
            c = MPDClient()
            c.connect(host=self.host, port=self.port)
            status = c.status()
            song = int(status   .get("song", 0))

            if (status["state"] == "pause") or (status["state"] == "stop"):
                text = ""
            else:
                try:
                    song = c.playlistinfo()[song]
                    song["time"] = "{0:.2f}".format(int(song.get("time", 1)) / 60)
                except IndexError:
                    song = {}

                format_args = song
                text = self.format
                for k, v in format_args.items():
                    text = text.replace("{" + k + "}", v)

                for sub in re.findall(r"{\S+?}", text):
                    text = text.replace(sub, "")
        except SocketError:
            text = "Failed to connect to mpd!"
        except CommandError:
            text = "Failed to authenticate to mpd!"
            c.disconnect()
        except ConnectionError:
            text = "Lost connection"

        if len(text) > self.max_width:
            text = text[:self.max_width-2] + ".."

        if self.text != text:
            transformed = True
            self.text = text
        else:
            transformed = False

        response = {
            'full_text': self.text,
            'transformed': transformed
        }

        if text == '':
            response['color'] = self.colors['stop']
        else:
            response['color'] = self.colors['play']
        print response
        return response

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    x = Py3status()
    config = {
        'color_good': '#00FF00',
        'color_bad': '#FF0000',
    }
    while True:
        x.current_track(config)
        sleep(2)
