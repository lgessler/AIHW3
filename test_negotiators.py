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

class LenientNegotiator(BaseNegotiator):
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0

        self.is_first = False
        self.iter = 0
        self.thresh = 0.3
        self.max_util = 0.0
        self.min_util = 0.0
        self.offer_index = 0

    def find_util(self, order):
        tmp = self.offer[:]
        self.offer = order[:]
        i = self.utility()
        self.offer = tmp
        return i

    def find_possibilities(self):
        #return sorted([(a,self.find_util(a)) for a in prm(self.preferences)],key=lambda x:x[1])
        L = [self.preferences[:]]
        outlist = []
        while True:
            tmp = L.pop(0)
            tmputil = self.find_util(tmp)
            if tmputil < self.thresh * self.find_util(self.preferences):
                break
            outlist.append((tmp,tmputil))

            for i in range(len(tmp)):
                for j in range(len(tmp)):
                    if i != j:
                        swapt = tmp[:]
                        swapt[i], swapt[j] = swapt[j], swapt[i]
                        if swapt not in L:
                            L.append(swapt)

        return sorted(outlist,key=lambda x: x[1])

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iter = 0
        self.sp = self.find_possibilities() 
        self.sp = self.sp[::-1]
        self.max_util = self.sp[0][1]
        self.min_util = self.thresh * self.max_util

    def make_offer(self, offer):
    #check if first in first iteration
        # assume no agent ever gives an offer of None
        if offer == None:
            self.is_first = True
        else:
            self.iter += 1

        #if last offer
        if self.iter == self.iter_limit:
            self.iter = 0
            if not self.is_first:
                self.offer = self.sp[0][0]
                return self.offer
            
            #Final accept
            elif self.find_util(offer) >= self.min_util:
                self.offer = offer[:]
                return offer
            #Final decline
            else:
                self.offer = self.sp[0][0]
                return self.offer

        # sorted possibilities
        if offer is None or (self.find_util(offer) < self.sp[self.offer_index][1]):
            self.offer = self.sp[self.offer_index][0]
            self.offer_index = (self.offer_index + 1) % len(self.sp)
            #If offer starts being bad, reset offers
            if self.sp[self.offer_index][1] < self.min_util:
                self.offer_index = 0
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

class CavingNegotiator(BaseNegotiator):
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

    def find_util(self, order):
        tmp = self.offer[:]
        self.offer = order[:]
        i = self.utility()
        self.offer = tmp
        return i

    def find_possibilities(self):
        #return sorted([(a,self.find_util(a)) for a in prm(self.preferences)],key=lambda x:x[1])
        L = [self.preferences[:]]
        outlist = []
        while True:
            tmp = L.pop(0)
            tmputil = self.find_util(tmp)
            if tmputil < self.thresh * self.find_util(self.preferences):
                break
            outlist.append((tmp,tmputil))

            for i in range(len(tmp)):
                for j in range(len(tmp)):
                    if i != j:
                        swapt = tmp[:]
                        swapt[i], swapt[j] = swapt[j], swapt[i]
                        if swapt not in L:
                            L.append(swapt)

        return sorted(outlist,key=lambda x: x[1])

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iter = 0
        self.sp = self.find_possibilities() 
        self.sp = self.sp[::-1]
        self.max_util = self.sp[0][1]
        self.min_util = self.thresh * self.max_util

    def make_offer(self, offer):
    #check if first in first iteration
        # assume no agent ever gives an offer of None
        if offer == None:
            self.is_first = True
        else:
            self.iter += 1

        #if last offer
        if self.iter == self.iter_limit:
            self.iter = 0
            if not self.is_first:
                self.offer = self.sp[0][0]
                return self.offer
            
            #Final accept
            else:
                self.offer = offer[:]
                return offer

        # sorted possibilities
        if offer is None or (self.find_util(offer) < self.sp[self.offer_index][1]):
            self.offer = self.sp[self.offer_index][0]
            self.offer_index = (self.offer_index + 1) % len(self.sp)
            #If offer starts being bad, reset offers
            if self.sp[self.offer_index][1] < self.min_util:
                self.offer_index = 0
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


class RandomNegotiator(BaseNegotiator):
    # Override the make_offer method from BaseNegotiator to accept a given offer 5%
    # of the time, and return a random permutation the rest of the time.   
    def make_offer(self, offer):
        if random() < 0.2 and offer:
            # Very important - we save the offer we're going to return as self.offer
            self.offer = offer[:]
            return offer
        else:
            ordering = self.preferences
            shuffle(ordering)
            self.offer = ordering[:]
            return self.offer



class RandomWithThresholdNegotiator(BaseNegotiator):
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