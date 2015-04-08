from functools import reduce
from itertools import permutations as prm
from negotiator_base import BaseNegotiator

class NaiveNegotiator:
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0

        self.is_first = False
        self.iter = 0
        self.thresh = 0.6
        self.max_util = 0.0
        self.min_util = 0.0
        self.offer_index = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.offered_before = []
        self.sp = reversed(sorted([(a,self.find_util(a)) for a in prm(self.preferences)],key=lambda x:x[1]))
        print "SP"
        print sp
        self.max_util = self.sp[0][1]
        self.min_util = self.thresh * self.max_util

    def find_util(self, order):
        tmp = self.offer[:]
        self.offer = order[:]
        i = self.utility()
        self.offer = tmp
        return i

    def make_offer(self, offer):
        #check if first in first iteration
        if self.iter == 0 and offer == None:
            self.is_first = True
        else:
            self.iter += 1

        #if last offer
        if self.iter == self.iter_limit:
            if !self.is_first:
                self.offer = self.sp[0][0]
                return self.offer
            
            #Final accept
            else if find_util(offer) >= self.min_util:
                self.offer = offer[:]
                return offer
            #Final decline
            else:
                self.offer = self.sp[0][0]
                return self.offer

        # sorted possibilities
        if offer is None or (self.find_util(offer) < self.sp[self.offer_index][1]):
            self.offer = self.sp[self.offer_index][1]
            self.offer_index += 1
            #If offer starts being bad, reset offers
            if self.sp[self.offer_index][1] < self.min_util:
                self.offer_index = 0
            #Add to offer list if not already there
            if self.offer not in self.offered_before:
                self.offered_before.append(self.offer)
            return self.offer

        self.offer = offer
        return self.offer

    def receive_utility(self, utility):
        self.opponents_utility = utility #literally never used

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        #If negotiation succeeded
        if results[0]:
            temp = 0.0
            if self.is_first:
                temp = results[1]
            else:
                temp = results[2]
            if temp > self.min_util:
                self.min_util = temp
        #If negotiation failed
        else:
            #Do nothing yet
            return
