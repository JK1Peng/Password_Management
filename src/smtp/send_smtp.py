"""
File: src/smtp/send_smtp.py

Author: Aaron Kersten, amk9398@rit.edu

Description: Contains code to interact with an SMTP server.
"""

import smtplib
import ssl


"""
@param: sender_email: sending email address
@param: password: sender's password
@param: receiver_email: receiver's email address
@param: subject: message subject
@param: body: message body
@return: 1 for success, 0 for failure

Sends an email using SMTP.
"""
def send(sender_email, password, receiver_email, subject, body):
    port = 465
    context = ssl.create_default_context()

    message = f"""\
    {subject}

    {body}"""

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            return 1
    except Exception as e:
        return 0
