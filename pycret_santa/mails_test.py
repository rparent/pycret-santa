import unittest

import pycret_santa.config
from pycret_santa.mails import BaseMail
from pycret_santa.guests import Guest


class BaseMailTests(unittest.TestCase):

  SENDER_NAME = "John Doe"
  SENDER_MAIL = "john@mail.com"
  SUBJECT = "foo"
  TEXT = "bar %(to)s %(gift_to)s"

  def setUp(self):
    self.sender = Guest(self.SENDER_NAME, self.SENDER_MAIL)
    self.bm = BaseMail(self.sender, self.SUBJECT, self.TEXT)

  def testGetSenderMail(self):
    self.assertEquals(self.bm.getSenderMail(), self.SENDER_MAIL)

  def testGetMailString(self):
    to = Guest("John", "john@mail.com")
    giftTo = Guest("Jack", "jack@mail.com")
    mailString = self.bm.getMailString(to, giftTo)
    self.assertEquals(type(mailString), str)
    self.assertIn("From: %s" % str(self.sender), mailString)
    self.assertIn("To: %s" % str(to), mailString)
    self.assertIn("Subject: %s" % self.SUBJECT, mailString)


class MailerTests(unittest.TestCase):
 # TODO: implement tests for this class
    pass


if __name__ == "__main__":
  unittest.main()
