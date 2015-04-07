from negotiator_base import BaseNegotiator
from random import random, shuffle

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class Selfish_Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.   
    def make_offer(self, offer):
        self.offer = self.preferences[:]
        return self.offer

    def calcUtility(offer):
        temp = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = temp
        return util

class Mostly_Selfish_Negotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.   
    threshold = 0.8

    def make_offer(self, offer):
        if offer != None and float(self.calc_utility(offer)) >= self.threshold * float(self.calc_utility(self.preferences)):
            self.offer = offer[:]
            return offer
        else:
            self.offer = self.preferences[:]
            return self.offer

    def calc_utility(self,offer):
        temp = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = temp
        return util