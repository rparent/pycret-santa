import itertools
import random

from pycret_santa import Separators


class Guest(object):

  def __init__(self, name, email):
    self.name = name
    self.email = email
    self.unauthorizedMatches = set()

  def __str__(self):
    return "%s <%s>" % (self.name, self.email.encode("utf-8"))

  @classmethod
  def initFromFormattedString(cls, guestAsString):
    tokens = guestAsString.split(Separators.MAIL_LEFT)
    name = tokens[0].strip().encode("utf-8")
    email = tokens[1].strip().strip(Separators.MAIL_RIGHT)
    return cls(name, email)

  def isMatchAuthorized(self, guest):
    return (guest.name not in self.unauthorizedMatches) \
           and (guest.name != self.name)

  def getSummary(self):
    stringSummary = self.__str__()
    if self.unauthorizedMatches:
      stringSummary += " (will not offer present to %s)" % \
                       ", ".join(self.unauthorizedMatches)
    return stringSummary


class GuestMatcher(object):

  def __init__(self, guestList):
    self.guestList = guestList

  def _isPermutationValid(self, shuffledList):
    for i in xrange(len(self.guestList)):
      if not self.guestList[i].isMatchAuthorized(shuffledList[i]):
        return False
    return True

  def _getMatchesAsDict(self, shuffledList):
    return {self.guestList[i].name: shuffledList[i] for i in \
            xrange(len(self.guestList))}

  def getMatches(self):
    shuffledList = self.guestList[:]
    while not self._isPermutationValid(shuffledList):
      random.shuffle(shuffledList)
    return self._getMatchesAsDict(shuffledList)
