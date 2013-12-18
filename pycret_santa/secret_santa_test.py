import sys
import unittest

from mock import patch
import mox

from pycret_santa.config import MailParameters
from pycret_santa.guests import Guest
from pycret_santa.mails import BaseMail, Mailer
from pycret_santa.secret_santa import SecretSanta, SecretSantaFactory


class SecretSantaTests(unittest.TestCase):

  def setUp(self):
    self.guestList = [Guest(name, "%s@domain.com" % name) for name in \
                      ["John", "Jack", "Julia"]]
    self.matches = {"John": self.guestList[1], "Jack": self.guestList[2],
                    "Julia": self.guestList[0]}
    self.mailer = mox.MockObject(Mailer)
    self.baseMail = BaseMail(Guest.initFromFormattedString(MailParameters.DEFAULT_SENDER),
                                MailParameters.DEFAULT_SUBJECT,
                        "%(to)s, you must offer a gift to %(gift_to)s")

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
