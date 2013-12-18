import unittest

from mock import patch

from pycret_santa.config import Separators, MailParameters, SmtpConfig, SecretSantaParameters
from pycret_santa.guests import Guest


class MailParametersTest(unittest.TestCase):

  SENDER_NAME = "John Doe"
  SENDER_MAIL = "john.doe@mail.com"
  SUBJECT = "foo"
  TEXT = "bar"

  def testInitFromDict(self):
    params = dict(text = self.TEXT,
                  subject = self.SUBJECT,
                  sender = self.SENDER_NAME + " " + Separators.MAIL_LEFT +
                           self.SENDER_MAIL + Separators.MAIL_RIGHT)
    mp = MailParameters()
    mp.initFromDict(params)
    self.assertEquals(mp.sender.name, self.SENDER_NAME)
    self.assertEquals(mp.sender.email, self.SENDER_MAIL)
    self.assertEquals(mp.text, self.TEXT)
    self.assertEquals(mp.subject, self.SUBJECT)

  def testInitFromDictWithNoOptionalParameters(self):
    params = dict(text = self.TEXT)
    mp = MailParameters()
    mp.initFromDict(params)
    defaultSender = Guest.initFromFormattedString(MailParameters.DEFAULT_SENDER)
    self.assertEquals(mp.sender.name, defaultSender.name)
    self.assertEquals(mp.sender.email, defaultSender.email)
    self.assertEquals(mp.text, self.TEXT)
    self.assertEquals(mp.subject, MailParameters.DEFAULT_SUBJECT)


class SmtpConfigTest(unittest.TestCase):

  HOST = "smtp.domain.com"
  PORT = 123
  USER = "user"
  PASSWORD = "pass"

  def testInitFromDict(self):
    params = dict(host = self.HOST,
                  port = self.PORT,
                  username = self.USER)
    sc = SmtpConfig()
    sc.initFromDict(params)
    self.assertEquals(sc.host, self.HOST)
    self.assertEquals(sc.port, self.PORT)
    self.assertEquals(sc.user, self.USER)
    self.assertEquals(sc.password, None)

  def testInitFromDictWithNoOptionalParameters(self):
    params = dict()
    sc = SmtpConfig()
    sc.initFromDict(params)
    self.assertEquals(sc.host, SmtpConfig.DEFAULT_HOST)
    self.assertEquals(sc.port, SmtpConfig.DEFAULT_PORT)
    self.assertEquals(sc.user, None)
    self.assertEquals(sc.password, None)

  @patch("getpass.getpass", lambda sc: SmtpConfigTest.PASSWORD)
  def testSetPassword(self):
    sc = SmtpConfig()
    sc.setPassword()
    self.assertEquals(sc.password, self.PASSWORD)


class SecretSantaParametersTest(unittest.TestCase):

  def setUp(self):
    self.ssp = SecretSantaParameters()
    self.ssp.guestList = [Guest(name, "%s@domain.com" % name) for name in \
                          ["John", "Jack", "Julia"]]

  def testHandleCouples(self):
    couples = ["Julia %s John" % Separators.COUPLE]
    self.ssp._handleCouples(couples)
    self.assertEquals(self.ssp.guestList[0].unauthorizedMatches, set(["Julia"]))
    self.assertEquals(self.ssp.guestList[1].unauthorizedMatches, set())
    self.assertEquals(self.ssp.guestList[2].unauthorizedMatches, set(["John"]))

  def testHandleNoMatchList(self):
    noMatches = ["Jack %s John" % Separators.NO_MATCH]
    self.ssp._handleNoMatchList(noMatches)
    self.assertEquals(self.ssp.guestList[0].unauthorizedMatches, set())
    self.assertEquals(self.ssp.guestList[1].unauthorizedMatches, set(["John"]))
    self.assertEquals(self.ssp.guestList[2].unauthorizedMatches, set())


if __name__ == "__main__":
  unittest.main()
