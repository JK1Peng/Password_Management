from captcha.image import ImageCaptcha
from definitions import ROOT_DIR
import os
import random


def generate_captcha(destination):
    image = ImageCaptcha(width=400, height=200)
    text = generate_captcha_text()
    data = image.generate(text)
    image.write(text, destination)
    return text


def generate_captcha_text():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
    text = ""
    for i in range(6):
        text += alphabet[random.randint(0, 35)]
    return text
