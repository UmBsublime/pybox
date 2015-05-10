
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
from mpd import MPDClient, ConnectionError
from socket import error as SocketError
from time import time

from widget_types import ScrollType, DynamicType
from variables import RED, GREEN, BLUE, CYAN, COMMAND_DELAY

class Py3status:
    """
    """
    # available configuration parameters
    cache_timeout = 2
    color = BLUE
    format_line1 = '{artist}-{title}'
    format_line2 = '{elapsed}/{duration}'
    host = 'localhost'
    max_width = 16
    port = '6600'

    def __init__(self):
        self.text = ['', '']
        try:
            self.c = MPDClient()
            self.c.connect(host=self.host, port=self.port)
        except ConnectionError:
            self.text[0] = "Can't connect"
            pass

    def disconnect(self):
        self.c.disconnect()

    def song_list(self, artist=''):
        song_l = self.c.list('Title', 'Artist', artist)
        return ScrollType(song_l, CYAN)

    def artist_list(self):
        artist_l = self.c.list('Artist')
        return ScrollType(artist_l, BLUE)

    def current_track_dyn(self):
        track = self.current_track()
        #color = self.current_track()

        d = DynamicType(self.current_track_text,track['color'])
        return d


    def current_track(self, colors=(GREEN, RED)):

        self.colors = {'color_good': colors[0],
                       'color_bad': colors[1]}
        line_1 = ""
        line_2 = ""

        status = self.c.status()
        print status
        song = int(status.get("song", 0))


        if (status["state"] == "pause") or (status["state"] == "stop"):
            line_1 = ""
        else:

            try:
                song_time = self.c.playlistinfo()[song]
                time = status['time'].split(':')
                print
                print song_time
                print
                song_time["elapsed"] = time[0]
                song_time["duration"] = time[1]
            except IndexError:
                song_time = {}

            format_args = song_time
            line_1 = self.format_line1
            line_2 = self.format_line2
            for k, v in format_args.items():
                line_1 = line_1.replace("{" + k + "}", v)
                line_2 = line_2.replace("{" + k + "}", v)

            for sub in re.findall(r"{\S+?}", line_1):
                line_1 = line_1.replace(sub, "")


        if len(line_1) > self.max_width:
            line_1 = line_1[:self.max_width-2] + ".."
        if len(line_2) > self.max_width:
            line_2 = line_2[:self.max_width-2] + ".."

        if (self.text[0] != line_1) or (self.text[1] != line_2):
            transformed = True
            self.text[0] = line_1
            self.text[1] = line_2
        else:
            transformed = False

        response = {
            'full_text': self.text,
            'transformed': transformed,
            'color': None
        }

        if line_1 == '':
            response['color'] = self.colors['color_bad']
        else:
            response['color'] = self.colors['color_good']
        print response
        return response

    def current_track_text(self):
        t = self.current_track()
        return t['full_text']

if __name__ == "__main__":
    """
    Test this module by calling it directly.
    """
    from time import sleep
    from pprint import pprint
    x = Py3status()
    a = x.artist_list()
    pprint(a.content)
    s = x.song_list(a.content[0])
    pprint(s.content)
    config = {
        'color_good': GREEN,
        'color_bad': RED,
    }
    while True:
        x.current_track(config)
        sleep(COMMAND_DELAY)

    x.disconnect()