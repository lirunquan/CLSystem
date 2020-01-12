# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from server.settings import UTILS_DIR
from manager import Manager
import os
import random


class VertificationCode:
    def __init__(self, width=150, height=45, code_length=5, font_size=30, points=20, lines=12, img_format='png'):
        self.img_data = None
        self.code = ''
        self.width = width
        self.height = height
        self.code_length = code_length
        self.font_size = font_size
        self.points = points
        self.lines = lines
        self.img_format = img_format
        self.image = Image.new(
            'RGB', (self.width, self.height), (250, 250, 250))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(os.path.join(
            UTILS_DIR, 'comic.ttf'), size=self.font_size)

    @staticmethod
    def get_random_color():
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return (r, g, b)

    @staticmethod
    def get_random_char():
        num = str(random.randint(0, 9))
        # low_alpha = chr(random.randint(97, 122))
        up_alpha = chr(random.randint(65, 90))
        return str(random.choice([num, up_alpha]))

    def draw_lines(self):
        for i in range(self.lines):
            x1, x2, y1, y2 = \
                random.randint(0, self.width), \
                random.randint(0, self.width), \
                random.randint(0, self.height), \
                random.randint(0, self.height)
            self.draw.line((x1, y1, x2, y2), fill=self.get_random_color())

    def draw_points(self):
        for i in range(self.points):
            self.draw.point(
                [random.randint(0, self.width),
                 random.randint(0, self.height)],
                fill=self.get_random_color())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.draw.arc((x, y, x + 4, y + 4), 0, 90,
                          fill=self.get_random_color())

    def get_code_image(self):
        self.code = Manager.get_random_code(length=self.code_length)
        for i in range(self.code_length):
            self.draw.text((5 + i * self.width / self.code_length, random.randint(0, 5)),
                           self.code[i],
                           self.get_random_color(),
                           font=self.font)
        self.draw_lines()
        self.draw_points()
        f = BytesIO()
        self.image.save(f, self.img_format)
        self.img_data = f.getvalue()
        f.close()
        return self.code, self.img_data
