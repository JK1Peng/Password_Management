"""
File: src/captcha.py

Author: Aaron Kersten, amk9398@rit.edu

Description: Can create a captcha image based off random text.
"""

from captcha.image import ImageCaptcha
import random


"""
@param: destination: file location for the png image
@return: the text used to create the captcha

Generates a captcha based off random text.
"""
def generate_captcha(destination):
    image = ImageCaptcha(width=400, height=200)
    text = generate_captcha_text()
    data = image.generate(text)
    image.write(text, destination)
    return text


"""
@return: random string

Generates a random string using lowercase letters and numbers.
"""
def generate_captcha_text():
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890"
    text = ""
    for i in range(6):
        text += alphabet[random.randint(0, 35)]
    return text
