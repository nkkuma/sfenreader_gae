#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# sfen.py Copyright 2015-2016 shibacho
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import urllib.parse
import logging
import re
from time import time

from sfenlib import u2utf8

class TwiimgHandler():
    DEFAULT_TITLE = u'局面図'
    EDITING_STRING_EN = u'Edit another dialog from this dialog'
    EDITING_STRING_JA = u'この局面を引き継いで別の局面を作る'

    def __init__(self, url_root, args, query_string):
        self.url_root = url_root
        self.args = args
        self.query_string = query_string.decode('utf-8')

    def get(self):
        print(self.url_root)
        print(self.args)
        print(self.query_string)
        print(type(self.args))

        path = self.url_root
        
        sfen_raw = self.args.get('sfen')
        sfen = urllib.parse.unquote(sfen_raw)
        sfenurl = "{}sfen?{}".format(path, self.query_string)
        resizeurl = "{}resize?{}".format(path, self.query_string)

        sfen = sfen.replace('\r','')
        sfen = sfen.replace('\n','')

        black_name_raw = urllib.parse.unquote(self.args.get('sname', ''))
        white_name_raw = urllib.parse.unquote(self.args.get('gname', ''))
        title_raw = self.args.get('title', '')
        black_name = u2utf8(black_name_raw)
        white_name = u2utf8(white_name_raw)
        if title_raw != "":
            title = u2utf8(urllib.parse.unquote(title_raw))
        else:
            title = self.DEFAULT_TITLE

        height = 421
        # If board has no name, the image height is smaller.
        if black_name == '' and white_name == '' and self.args.get('title') == '':
            height = 400

        response = ""
        response += '<!DOCTYPE html>'
        response += '<html>\n<head>\n'
        response += '<meta name="twitter:id" content="{}" />\n'.format(str(time())[:-3])
        response += '<meta name="twitter:card" content="summary_large_image" />\n'
        response += '<meta name="twitter:site" content="@sfenreader_gae" />\n'
        response += '<meta name="twitter:description" content="@sfenreader_gae" />\n'
        response += '<meta name="twitter:title" content="{}" />\n'.format(title)
        if black_name != '' and white_name != '':
            response += '<meta name="twitter:description" content="{} vs {}" />\n'.format(black_name, white_name)
        else:
            response += '<meta name="twitter:description" content="{}" />\n'.format(title)
        
        # response += ('<meta name="twitter:image" content="{}" />\n'.format(sfenurl))
        response += '<meta name="twitter:image" content="{}" />\n'.format(resizeurl)
        # response += ('<meta name="twitter:image:width" content="400" />\n')
        response += '<meta name="twitter:image:width" content="842" />\n'
        response += '<meta name="twitter:image:height" content="421" />\n'
        # response += ('<meta name="twitter:url" content="{}" />\n'.format(sfenurl))
        response += '<meta name="twitter:url" content="{}" />\n'.format(resizeurl)
        response += '<meta charset="UTF-8" />\n'
        response += '</head>\n<body>\n'
        response += '<p>\n<div style="text-align:center;">{}</div><br>\n'.format(title)
        response += '<img src="{}" /><br>\n'.format(sfenurl)
        query = self.create_sfen_query(sfen_raw, black_name_raw, white_name_raw, title_raw)
        response += u'<span style="text-align:left;"><a href="./ja/create_board.html{}">{}</a></span><br>'.format(query, self.EDITING_STRING_JA)
        response += u'<span style="text-align:left;"><a href="./en/create_board.html{}">{}</a></span><br>'.format(query, self.EDITING_STRING_EN)
        response += '</body>\n</html>\n'
        return (200, response)

    def create_sfen_query(self, sfen, black_name, white_name, title):
        query = ""
        if sfen != "":
            query += "sfen=" + sfen + "&"
        if black_name != "":
            query += "sname=" + black_name + "&"
        if white_name != "":
            query += "gname=" + white_name + "&"
        if title != "":
            query += "title=" + title + "&"
        if query[-1] == "&":
            query = "?" + query[:-1]
        return query

