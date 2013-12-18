# coding: utf-8
from email.mime.text import MIMEText
import smtplib


class BaseMail(object):

  def __init__(self, sender, subject, text):
    self.sender = sender
    self.subject = subject
    self.text = text

  def getSenderMail(self):
    return self.sender.email

  def getMailString(self, to, giftTo):
    text = self.text % {"to": to.name, "gift_to": "<b>%s</b>" % giftTo.name}
    message = MIMEText(text.replace("\n", "<br />"), 'html', 'utf-8')
    message["Subject"] = self.subject
    message["From"] = str(self.sender)
    message["To"] = str(to)
    return message.as_string()


class Mailer(object):

  def __init__(self, host, port, username, password):
    self._host = host
    self._port = port
    self._username = username
    self._password = password
    self._smtpClient = smtplib.SMTP(self._host, self._port)

  def __del__(self):
    self.closeConnection()

  def startConnection(self):
    self._smtpClient.ehlo()
    self._smtpClient.starttls()
    self._smtpClient.ehlo()
    self._smtpClient.login(self._username, self._password)

  def closeConnection(self):
    self._smtpClient.close()

  def sendMail(self, senderMail, toMail, message):
    self._smtpClient.sendmail(senderMail, toMail, message)
