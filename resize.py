#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# sfen.py Copyright 2016 shibacho
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


from PIL import Image

import urllib.request
import logging

from util import *

class ResizeHandler():
    WIDTH = 1520
    HEIGHT = 800

    def __init__(self, url_root, args, query_string):
        self.url_root = url_root
        self.args = args
        self.query_string = query_string.decode('utf-8')

    def get(self):
        ### height:800px width:800px
        ### width will be about 1520px
        # self.response.headers['Content-Type'] = 'image/png'
        ### put out resized png image which matches Twitter card.
        ### Basic concept
        ### 1: Prepare white back png which width is 1520px, height is 800px.
        ### 2: put diagram image center of the images

        ### Make white background image (1520x800 px)
        image = Image.open('img/whitebase.png').resize((self.WIDTH, self.HEIGHT))

        url = self.url_root + 'sfen?' + self.query_string

        diagram_img = urllib.request.urlopen(url).read()
        diagram_img_obj = byte_array_to_image(diagram_img)
        x = (self.WIDTH - diagram_img_obj.size[0]) // 2

        image.paste(diagram_img_obj, (x,0))
        byte_image = image_to_byte_array(image)

        return (200, byte_image)
