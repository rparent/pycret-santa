# coding: utf-8
from email.mime.text import MIMEText
import getpass
import smtplib


class BaseMail(object):

  def __init__(self, mailParameters):
    self.sender = mailParameters.sender
    self.subject = mailParameters.subject
    self.text = mailParameters.text

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

  def __init__(self, smtpConfig):
    self._host = smtpConfig.host
    self._port = smtpConfig.port
    self._username = smtpConfig.user
    self._password = smtpConfig.password
    self._smtpClient = smtplib.SMTP(self._host, self._port)

  def setPassword(self):
    self._password = getpass.getpass("Please provide smtp password for user "
                                     "%s on server %s: " % (self._username,
                                                            self._host))

  def startConnection(self):
    if not self._password:
      self.setPassword()
    self._smtpClient.ehlo()
    self._smtpClient.starttls()
    self._smtpClient.ehlo()
    self._smtpClient.login(self._username, self._password)

  def closeConnection(self):
    self._smtpClient.close()

  def sendMail(self, senderMail, toMail, message):
    self._smtpClient.sendmail(senderMail, toMail, message)
