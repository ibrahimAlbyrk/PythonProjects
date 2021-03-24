import Memory
import smtplib
from email.message import EmailMessage


class Mail:
    from_mail = ""

    def __init__(self, from_mail):
        self.from_mail = from_mail

    def SendMail(self, message, to):
        msg = EmailMessage()
        msg.set_content(message)
        msg["subject"] = "Assistant Quinn"
        msg["to"] = to
        msg["from"] = self.from_mail
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self.from_mail, Memory.sendPassword)
        server.send_message(msg)
        server.quit()
