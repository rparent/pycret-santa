import unittest

from mock import patch

from pycret_santa.config import SmtpConfig
from pycret_santa.mails import BaseMail, Mailer
from pycret_santa.guests import Guest
from pycret_santa.utils import TestUtils


class BaseMailTests(unittest.TestCase):

  def setUp(self):
    self.helper = TestUtils()
    self.sender = self.helper.getSender()
    self.bm = self.helper.getBaseMail()

  def testGetSenderMail(self):
    self.assertEquals(self.bm.getSenderMail(), self.sender.email)

  def testGetMailString(self):
    guestList = self.helper.getGuestList()
    to = guestList[0]
    giftTo = guestList[1]
    mailString = self.bm.getMailString(to, giftTo)
    self.assertEquals(type(mailString), str)
    self.assertIn("From: %s" % str(self.sender), mailString)
    self.assertIn("To: %s" % str(to), mailString)
    self.assertIn("Subject: %s" % self.bm.subject, mailString)


class MailerTests(unittest.TestCase):

  PASSWORD = "pass"

  @patch("getpass.getpass", lambda sc: MailerTests.PASSWORD)
  def testSetPassword(self):
    config = SmtpConfig()
    mailer = Mailer(config)
    mailer.setPassword()
    self.assertEquals(mailer._password, self.PASSWORD)


if __name__ == "__main__":
  unittest.main()
