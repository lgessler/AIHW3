from functools import reduce
from itertools import permutations as prm
from negotiator_base import BaseNegotiator

class NaiveNegotiator(BaseNegotiator):
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

        self.opp_preference = []
        self.opp_max_util = -1.0
        self.opp_offers = []
        self.opp_confirmed_util = []
        self.opp_is_greedy = False
        self.opp_offering_pref = False
        self.opp_greed_count = 0

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
            #Give final offer
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
        if utility > self.opp_max_util:
            self.opp_max_util = utility
            self.opp_offering_pref = True



    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.iter = 0
        
        #If negotiation SUCCEEDED
        if results[0]:
            #If I went FIRST
            if self.is_first:
                my_score = results[1]
                opp_score = results[2]

                #If I LOST
                if my_score < opp_score:
                    #If negotiation dragged to last round = 
                    if results[3] == self.iter_limit:
                        return
                    #If negotiation aggreed midway
                    else:
                        return
                #If I WON
                elif my_score > opp_score:
                    #If negotiation dragged to last round
                    if results[3] == self.iter_limit:
                        if temp > self.min_util:
                            self.min_util = temp
                    #If negotiation aggreed midway
                    else:
                        continue
                #If we DREW
                else:
                    #If negotiation dragged to last round
                    if results[3] == self.iter_limit:
                        if temp > self.min_util:
                            self.min_util = temp
                    #If negotiation aggreed midway
                    else:
                        if temp > self.min_util:
                            self.min_util = temp
            #If I went SECOND
            else:
                my_score = results[2]
                opp_score = results[1]

                #If I LOST
                if my_score < opp_score:
                    #If negotiation dragged to last round
                    if results[3] == self.iter_limit:
                        if temp > self.min_util:
                            self.min_util = temp
                    #If negotiation aggreed midway
                    else:
                        continue
                #If I WON
                elif my_score > opp_score:
                    #If negotiation dragged to last round (Opponent accepted last offer)
                    if results[3] == self.iter_limit:
                        if temp > self.min_util:
                            self.min_util = temp
                    #If negotiation aggreed midway
                    else:
                        continue
                #If we DREW
                else:
                    #If negotiation dragged to last round
                    if results[3] == self.iter_limit:
                        if temp > self.min_util:
                            self.min_util = temp
                    #If negotiation aggreed midway
                    else:
                        if temp > self.min_util:
                            self.min_util = temp
            
        #If negotiation FAILED
        else:
            #Do nothing yet
            return
