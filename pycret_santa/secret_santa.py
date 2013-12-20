import sys

from pycret_santa.config import SecretSantaParameters
from pycret_santa.guests import Guest, GuestMatcher
from pycret_santa.mails import BaseMail, Mailer


class SecretSanta(object):

  _SUMMARY_TEMPLATE = """
*********************
*    SECRET SANTA   *
*********************
The mail will be send by %(sender)s
To:
%(guests)s

Subject: %(subject)s

Text:
%(text)s

"""

  def __init__(self, guestList, matches, mailer, baseMail):
    self.guestList = guestList
    self.matches = matches
    self.mailer = mailer
    self.baseMail = baseMail

  def _printSummary(self):
    print self._SUMMARY_TEMPLATE % {"sender": str(self.baseMail.sender),
                                    "guests": "\n".join(["\t- %s" % \
                                        guest.getSummary() for guest in \
                                        self.guestList]),
                                    "subject": self.baseMail.subject,
                                    "text": self.baseMail.text % \
                                        {'to': 'Name1', 'gift_to': 'Name2'}}

  def _waitForGo(self):
    self._printSummary()
    answer = raw_input("Is it all ok? [y/N]\n")
    if answer.lower() not in ["y", "yes"]:
      sys.exit(1)

  def run(self):
    self._waitForGo()
    self.mailer.startConnection()
    try:
      for guest in self.guestList:
        print "Sending mail to %s..." % guest
        self.mailer.sendMail(self.baseMail.getSenderMail(), guest.email,
                             self.baseMail.getMailString(guest,
                                                      self.matches[guest.name]))
    finally:
      self.mailer.closeConnection()


class SecretSantaFactory(object):

  def getFromConfigFile(self, filePath):
    params = SecretSantaParameters()
    params.initFromFile(filePath)
    return self._getSecretSanta(params)

  def getFromCommandLine(self):
    params = SecretSantaParameters().initFromCommandLine()
    return self._getSecretSanta(params)

  def _getSecretSanta(self, params):
    guestList = params.guestList
    matches = GuestMatcher(guestList).getMatches()
    mailer = Mailer(params.smtp)
    baseMail = BaseMail(params.mail)
    return SecretSanta(guestList, matches, mailer, baseMail)


def main():
  if len(sys.argv) == 2:
    secretSanta = SecretSantaFactory().getFromConfigFile(sys.argv[1])
  else:
    print "Usage: secretsanta [<path_to_config_file>]"
    sys.exit(1)
  secretSanta.run()


if __name__ == "__main__":
  main()
