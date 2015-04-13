from negotiator_base import BaseNegotiator
from random import random, shuffle

class mqn2at(BaseNegotiator):
    threshold = 0.5
    is_first = False
    iter_num = 0

    def calc_utility(self,offer):
        temp = self.offer
        self.offer = offer
        util = self.utility()
        self.offer = temp
        return util

    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.   
    def make_offer(self, offer):
        if offer == None:
            self.is_first = True
        else:
            self.iter_num += 1

        #if last offer
        if self.iter_num == self.iter_limit:
            self.iter_num = 0
            if not self.is_first:
                self.offer = self.preferences
                return self.offer
            
            #Final accept
            else:
                self.offer = offer[:]
                return offer

        if offer != None and float(self.calc_utility(offer)) >= self.threshold * float(self.calc_utility(self.preferences)):
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer[:]
            return offer
        else:
            ordering = self.preferences
            shuffle(ordering)
            while float(self.calc_utility(ordering)) < self.threshold * float(self.calc_utility(self.preferences)):
                shuffle(ordering)
            self.offer = ordering[:]
            return self.offer

    def receive_results(self, results):
        self.is_first = False
        self.iter_num = 0
