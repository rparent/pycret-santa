import sys
import unittest

from mock import patch
import mox

from pycret_santa.config import MailParameters
from pycret_santa.guests import Guest
from pycret_santa.mails import BaseMail, Mailer
from pycret_santa.secret_santa import SecretSanta, SecretSantaFactory
from pycret_santa.utils import TestUtils


class SecretSantaTests(unittest.TestCase):

  def setUp(self):
    helper = TestUtils()
    self.guestList = helper.getGuestList()
    self.matches = helper.getMatchesDict()
    self.mailer = mox.MockObject(Mailer)
    self.baseMail = helper.getBaseMail()

  @patch("__builtin__.raw_input", lambda x: "y")
  def testRun(self):
    self.mailer.startConnection()
    for guest in self.guestList:
      self.mailer.sendMail(self.baseMail.getSenderMail(), guest.email,
                           self.baseMail.getMailString(guest,
                                                      self.matches[guest.name]))
    self.mailer.closeConnection()

    mox.Replay(self.mailer)
    secretSanta = SecretSanta(self.guestList, self.matches, self.mailer,
                              self.baseMail)
    secretSanta.run()
    mox.Verify(self.mailer)


if __name__ == "__main__":
  unittest.main()
