from functools import reduce
from itertools import permutations as prm

class NaiveNegotiator:
    def __init__(self):
        self.preferences = []
        self.offer = []
        self.iter_limit = 0

    def initialize(self, preferences, iter_limit):
        self.preferences = preferences
        self.iter_limit = iter_limit
        self.offered_before = []
        self.sp = sorted([(a,self.find_util(a)) for a in prm(self.preferences)],key=lambda x:x[1])

    def find_util(self, order):
        tmp = self.offer[:]
        self.offer = order[:]
        i = self.utility()
        self.offer = tmp
        return i

    def make_offer(self, offer):
        # sorted possibilities
        if offer is None or (self.find_util(offer) <= self.sp[-1][1]): #or len(self.offered_before) == 0:
            self.offer = self.sp.pop()[0]
            self.offered_before.append(self.offer)
            return self.offer

        self.offer = offer
        return self.offer

    def receive_utility(self, utility):
        self.opponents_utility = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        pass

    # utility(self : BaseNegotiator) --> Float
        # Return the utility given by the last offer - Do not modify this method.
    def utility(self):
        total = len(self.preferences)
        return reduce(lambda points, item: points + ((total / (self.offer.index(item) + 1)) - abs(self.offer.index(item) - self.preferences.index(item))), self.offer, 0)


