from functools import reduce
from itertools import permutations as prm
from negotiator_base import BaseNegotiator

class AccommodatingNegotiator(BaseNegotiator):
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0

        self.is_first = False
        self.iter = 0
        self.max_util = 0.0
        self.offer_index = 0
        self.offer_step_size = 1

        #Four thresholds:
        self.offer_thresh = 0.6
        self.accept_thresh = 0.5
        self.last_offer_thresh = 0.3
        self.last_accept_thresh = 0.2
        self.highest_opp_offer = [] #best offer the opponents give that are above last_offer_thresh but below accept_thresh
        self.highest_opp_offer_util = 0.0 #highest utility of best offer from opponent
        self.accepted_midway = False

        self.opp_preference = []
        self.opp_max_util = -1.0
        self.opp_offers = []


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
            if tmputil < self.offer_thresh * self.find_util(self.preferences):
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
        self.__init__()
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.iter = 0
        self.sp = self.find_possibilities() 
        self.sp = self.sp[::-1]
        self.max_util = self.sp[0][1]

    def make_offer(self, offer):
    #check if first in first iteration
        # assume no agent ever gives an offer of None
        if offer == None:
            self.is_first = True
        else:
            self.iter += 1
            #Save opponent offer
            opp_util = self.find_util(offer)
            if opp_util >= self.last_offer_thresh * self.max_util and opp_util > self.highest_opp_offer_util:
                self.highest_opp_offer = offer
                self.highest_opp_offer_util = opp_util

        #if last offer
        if self.iter == self.iter_limit:
            #Give final offer
            if not self.is_first:
                #If opponent hasn't given reasonable offer, spit back preferences
                if self.highest_opp_offer == []:
                    self.offer = self.sp[0][0]
                    return self.offer
                #If opponent has given us reasonable offer prior, offer back
                else:
                    self.offer = self.highest_opp_offer[:]
                    return self.offer
            
            #Final accept
            elif self.find_util(offer) >= self.last_accept_thresh * self.max_util:
                self.offer = offer[:]
                return offer
            #Final decline
            else:
                self.offer = self.sp[0][0]
                return self.offer

        # sorted possibilities
        if offer is None or self.find_util(offer) < self.accept_thresh * self.max_util:
            self.offer = self.sp[self.offer_index][0]
            self.offer_index = (self.offer_index + self.offer_step_size) % len(self.sp)           
            if self.sp[self.offer_index][1] < self.offer_thresh * self.max_util:
                self.offer_index = 0
            return self.offer

        self.offer = offer
        self.accepted_midway = True
        return self.offer

    def receive_utility(self, utility):
        if utility > self.opp_max_util:
            self.opp_max_util = utility
            self.opp_offering_pref = True

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
    # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.iter = 0
        self.offer_index = 0
        self.opp_offers = []
        self.accepted_midway = False
        
        #If negotiation SUCCEEDED
        if results[0]:
            #If I went FIRST
            if self.is_first:
                my_score = results[1]
                opp_score = results[2]

                #If I LOST
                if my_score < opp_score:
                    #If negotiation dragged to last round = accepted last offer
                    if results[3] == self.iter_limit:
                        if my_score < 0.8 * opp_score:
                            self.last_accept_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.last_accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and we accepted
                    elif self.accepted_midway:
                        if my_score < 0.8 * opp_score:
                            self.accept_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and opponent accepted
                    else:
                        if my_score < 0.8 * opp_score:
                            self.offer_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.offer_thresh = float(my_score) / float(self.max_util)
                #If I WON or DREW
                elif my_score >= opp_score:
                    #If negotiation dragged to last round = accepted last offer
                    if results[3] == self.iter_limit:
                        self.last_accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and we accepted
                    elif self.accepted_midway:
                        self.accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and opponent accepted
                    else:
                        self.offer_thresh = float(my_score) / float(self.max_util)
            #If I went SECOND
            else:
                my_score = results[2]
                opp_score = results[1]

                #If I LOST
                if my_score < opp_score:
                    #If negotiation dragged to last round = made the last offer
                    if results[3] == self.iter_limit:
                        if my_score < 0.8 * opp_score:
                            self.last_offer_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.last_offer_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and we accepted
                    elif self.accepted_midway:
                        if my_score < 0.8 * opp_score:
                            self.accept_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and opponent accepted
                    else:
                        if my_score < 0.8 * opp_score:
                            self.offer_thresh = float(my_score) / float(self.max_util) + 0.05
                        else:
                            self.offer_thresh = float(my_score) / float(self.max_util)
                #If I WON or DREW
                elif my_score >= opp_score:
                    #If negotiation dragged to last round = accepted last offer
                    if results[3] == self.iter_limit:
                        self.last_offer_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and we accepted
                    elif self.accepted_midway:
                        self.accept_thresh = float(my_score) / float(self.max_util)
                    #If negotiation aggreed midway and opponent accepted
                    else:
                        self.offer_thresh = float(my_score) / float(self.max_util)
            
        #If negotiation FAILED
        else:
            self.offer_step_size += 1
            #if self.last_accept_thresh > 0.0:
            #    self.last_accept_thresh -= 0.05
