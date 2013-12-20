
from pycret_santa import Separators
from pycret_santa.config import MailParameters
from pycret_santa.guests import Guest
from pycret_santa.mails import BaseMail


class TestUtils(object):

  NAMES = ["John", "Jack", "Julia"]
  SENDER_NAME = "John Doe"
  SENDER_EMAIL = "john@mail.com"
  SUBJECT = "test"
  TEXT = "%(to)s, you must offer a gift to %(gift_to)s"

  def __init__(self):
    self.guestList = None

  def getGuestList(self):
    guestList = [Guest(name, "%s@domain.com" % name) for name in self.NAMES]
    guestList[0].unauthorizedMatches.add(self.NAMES[1])
    self.guestList = guestList
    return guestList

  def getMatchesDict(self):
    if not self.guestList:
      _ = self.getGuestList()
    return {self.NAMES[0]: self.guestList[2],
            self.NAMES[1]: self.guestList[0],
            self.NAMES[2]: self.guestList[1]}

  def getSender(self):
    return Guest(self.SENDER_NAME, self.SENDER_EMAIL)

  def getSenderString(self):
    return (self.SENDER_NAME + " " + Separators.MAIL_LEFT + self.SENDER_EMAIL +
            Separators.MAIL_RIGHT)

  def getBaseMail(self):
    params = MailParameters(self.getSender(), self.SUBJECT, self.TEXT)
    return BaseMail(params)

