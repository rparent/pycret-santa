import unittest

from pycret_santa.config import Separators
from pycret_santa.guests import Guest, GuestMatcher


class GuestTests(unittest.TestCase):

  NAME = "John Doe"
  MAIL = "john@mail.com"

  def testInitFromFormattedString(self):
    fs = (self.NAME + Separators.MAIL_LEFT + "   " + self.MAIL +
         Separators.MAIL_RIGHT + " ")
    g = Guest.initFromFormattedString(fs)
    self.assertEquals(g.name, self.NAME)
    self.assertEquals(g.email, self.MAIL)

  def testIsMatchAuthorized(self):
    g = Guest(self.NAME, self.MAIL)
    g.unauthorizedMatches.add("Jack")
    self.assertFalse(g.isMatchAuthorized(g))
    self.assertFalse(g.isMatchAuthorized(Guest("Jack", "jack@mail.com")))


class GuestMatcherTests(unittest.TestCase):

  def setUp(self):
    guestList = [Guest(name, "%s@domain.com" % name) for name in \
                 ["John", "Jack", "Julia"]]
    guestList[0].unauthorizedMatches.add("Jack")
    self.gm = GuestMatcher(guestList)

  def testIsPermutationValid(self):
    invalidPermutation1 = [self.gm.guestList[0],
                           self.gm.guestList[2],
                           self.gm.guestList[1]]
    invalidPermutation2 = [self.gm.guestList[1],
                           self.gm.guestList[2],
                           self.gm.guestList[0]]
    validPermutation = [self.gm.guestList[2],
                        self.gm.guestList[0],
                        self.gm.guestList[1]]
    self.assertTrue(self.gm._isPermutationValid(validPermutation))
    self.assertFalse(self.gm._isPermutationValid(invalidPermutation1))
    self.assertFalse(self.gm._isPermutationValid(invalidPermutation2))

  def testGetMatches(self):
    matches = self.gm.getMatches()
    self.assertEquals(matches, {"John": self.gm.guestList[2],
                                 "Jack": self.gm.guestList[0],
                                 "Julia": self.gm.guestList[1]})


if __name__ == "__main__":
  unittest.main()
