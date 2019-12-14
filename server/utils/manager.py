# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from django.template import loader
from server.settings import UTILS_DIR, DEFAULT_FROM_EMAIL, SERVER_HOST
from django.core.mail import send_mail, send_mass_mail
from apps.record.models import CertificationSentRecord, EmailSentRecord
import os
import uuid
import hashlib


class Manager:
    def __init__(self):
        pass

    @staticmethod
    def get_random_char():
        num = str(random.randint(0, 9))
        # low_alpha = chr(random.randint(97, 122))
        up_alpha = chr(random.randint(65, 90))
        return str(random.choice([num, up_alpha]))

    @staticmethod
    def get_random_code(length=5):
        code = ''
        for i in range(length):
            code += Manager.get_random_char()
        return code

    @staticmethod
    def get_md5_str():
        uuid_val = uuid.uuid4()
        uuid_str = str(uuid_val).encode("utf-8")
        md5 = hashlib.md5()
        md5.update(uuid_str)
        return md5.hexdigest()


class VerificationCodeGenerator:
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
        self.image = Image.new('RGB', (self.width, self.height), (250, 250, 250))
        self.draw = ImageDraw.Draw(self.image)
        self.font = ImageFont.truetype(os.path.join(UTILS_DIR, 'comic.ttf'), size=self.font_size)

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
                [random.randint(0, self.width), random.randint(0, self.height)],
                fill=self.get_random_color())
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.draw.arc((x, y, x + 4, y + 4), 0, 90, fill=self.get_random_color())

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


class EmailManager(Manager):
    def __init__(self, account, receive: list):
        super().__init__()
        self.account = account
        self.token = ''
        self.code = ''
        self.email_receiver = receive

    def send(self, email_type):
        if email_type == 'certificate':
            if not self.send_certificate_email():
                self.save_sent_record(email_type, False)
                return
        self.save_sent_record(email_type)

    def load_html(self, html_file, params):
        template = loader.get_template(html_file)
        return template.render(params)

    def send_certificate_email(self):
        self.token = self.get_md5_str()
        self.code = self.get_random_code(length=8)
        url = SERVER_HOST + "/user/active?token={0}&code={1}".format(self.token, self.code)
        email_content = self.load_html(html_file='/email/certificate.html',
                                       params={"active_url": url})
        email_title = "认证邮箱并激活"
        email_sender = DEFAULT_FROM_EMAIL
        ret = send_mail(subject=email_title,
                        from_email=email_sender,
                        message='',
                        html_message=email_content,
                        recipient_list=self.email_receiver)
        return ret == 1

    def save_sent_record(self, email_type, success=True):
        if email_type == 'certificate':
            record = CertificationSentRecord(
                user=self.account,
                recipients=';'.join(self.email_receiver),
                token=self.token,
                active_code=self.code,
                success=success
            )
            record.save()
