"""
File: src/smtp/email_controller.py

Author: Aaron Kersten, amk9398@rit.edu

Description: Contains all functions and logic the GUI needs to send emails
             to user accounts.
"""

from src.smtp.send_smtp import send


"""
@return: email address, app password

Get sending email credentials.
"""
def get_credentials():
    credentials = []
    with open("../../smtp/credentials") as file:
        for line in file:
            split_line = line.replace("\n", "").split(": ")
            credentials.append(split_line[1])
    return credentials


"""
@param: email: destination address--the user's email
@param: code: verification code
@return: 1 for success, 0 for failure

Send verification code to user's email address.
"""
def send_verification_email(email, code):
    project_email, app_password = get_credentials()
    subject = "Verification code: 655 Password Manager Project"
    body = f"Your code is : {code}"
    return send(project_email, app_password, email, subject, body)


"""
@param: email: destination address--the user's email
@param: hint: password hint
@return: 1 for success, 0 for failure

Send password hint to the user's email address.
"""
def send_hint_email(email, hint):
    project_email, app_password = get_credentials()
    subject = "Password hint: 655 Password Manager Project"
    body = f"Your hint is : {hint}"
    return send(project_email, app_password, email, subject, body)
