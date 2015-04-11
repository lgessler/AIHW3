from negotiator_base import BaseNegotiator
from random import randint, random
import copy

# Example negotiator implementation, which randomly chooses to accept
# an offer or return with a randomized counteroffer.
# Important things to note: We always set self.offer to be equal to whatever
# we eventually pick as our offer. This is necessary for utility computation.
# Second, note that we ensure that we never accept an offer of "None".
class A3Negotiator(BaseNegotiator):
    # Constructor - Note that you can add other fields here; the only 
    # required fields are self.preferences and self.offer
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0
        self.iter_count = 0
        self.end_pref = 0
        self.aggr_lim = 2
        self.results = []
        self.rd_count = 0
        self.opp_aggr = False
        self.reply_to_aggr = False
        self.best_offer_aggr = [None, -999999999999]
        self.concede = False

    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences 
    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        if(self.opp_aggr == False):
            self.offer = self.preferences
        self.end_pref = len(self.preferences) - 1
        self.iter_count = 0
        #elf.aggr_lim = 2
        self.aggr_lim = len(preferences) // 2

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list), 
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        #print("self: " + str(self.offer) + " " + str(self.preferences))
        #Keep track of iterations
        self.iter_count = self.iter_count + 1
        offer = copy.deepcopy(offer)
        #Accept if offer is out offer/preference
        if offer == self.offer or offer == self.preferences:
            return offer

        #if first offer, send pref
        if offer == None:
            return self.preferences

        if(self.concede == True):
            if random() < 0.5 and offer:
                return offer

        #if we sense aggressive, keep track of offers and save minimal
        if self.opp_aggr == True:
            #print("util")
            tmp_offer = self.offer
            self.offer = offer
            utility_given_offer = self.utility()
            self.offer = tmp_offer
            #print(str(utility_given_offer))
            #print(str(self.utility()))
            
            if self.best_offer_aggr[1] < utility_given_offer:
                #print(str(self.offer) + " " + str(utility_given_offer))
                new_offer = (offer, utility_given_offer)
                self.best_offer_aggr[0] = offer
                self.best_offer_aggr[1] = utility_given_offer
                self.offer = self.best_offer_aggr[0]
        #send back an offer we know they want but maximizes our utility
        if self.reply_to_aggr == True and self.utility() > len(self.preferences):
            #print("hi")
            return self.offer

        #if last turn, blast preference
        if self.iter_count == self.iter_limit - 1 and self.reply_to_aggr == False:
            return self.preferences
        #otherwise swap minimally
        else:
            swap1 = randint(0, self.aggr_lim)
            swap2 = randint(0, self.aggr_lim)
            tmp = self.offer[swap1]
            self.offer[swap1] = self.offer[swap2]
            self.offer[swap2] = tmp
            return self.offer

    def receive_results(self, results):
        
        self.rd_count += 1
        #keep track of results
        self.results.append((results[0], results[3]))
        #if we failed last 3 probably they are aggressive too
        if self.rd_count > 2 and self.concede == False:
            num_result_end = 0
            for i in self.results:
                if i[0] == False and i[1] >= self.iter_limit - 1:
                    num_result_end += 1
            if(num_result_end > (self.rd_count * (2/3))):
                self.opp_aggr = True
        #if we have not won much after 6 rounds this person is too aggressive
        if self.rd_count > 6 and self.concede == False:
            for i in self.results:
                if i[0] == False and i[1] >= self.iter_limit - 1:
                    num_result_end += 1
            if(num_result_end > (self.rd_count * (9/10))):
                self.concede = True
                    
        #track for 2 more rounds and then respond with our most optimal
        if self.rd_count > 4 and self.opp_aggr == True and self.concede == False:
            self.reply_to_aggr = True
        self.initialize(self.preferences, self.iter_limit)
