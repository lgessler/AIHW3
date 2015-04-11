from negotiator_base import BaseNegotiator
import random
import copy

class MinLoss_Negotiator(BaseNegotiator):

    def __init__(self):
        super(MinLoss_Negotiator, self).__init__()
        self.curr_num_iters = 0

        # Contains a history of the raw (non normalized opponent's utility)
        # This is only for determining if we should update the opponent's
        # preference.
        self.curve_len = 0.95
        self.max_opponent_util = -10000000
        self.prev_opponent_util = 0
        self.i_went_first = False
    # initialize(self : BaseNegotiator, preferences : list(String), iter_limit : Int)
        # Performs per-round initialization - takes in a list of items, ordered by the item's
        # preferability for this negotiator
        # You can do other work here, but still need to store the preferences 
    def initialize(self, preferences, iter_limit):
        super(MinLoss_Negotiator, self).initialize(preferences, iter_limit)
        self.curr_num_iters = 0
        self.offer = self.preferences[:]
        self.my_max_util = self.utility()

    # make_offer(self : BaseNegotiator, offer : list(String)) --> list(String)
        # Given the opposing negotiator's last offer (represented as an ordered list), 
        # return a new offer. If you wish to accept an offer & end negotiations, return the same offer
        # Note: Store a copy of whatever offer you make in self.offer at the end of this method.
    def make_offer(self, offer):
        # The curve we are sampling is 1 - x^2
        self.curr_num_iters += 1

        if(not offer):
            self.offer = self.preferences
            self.i_went_first = True
            return self.preferences

        offer = copy.deepcopy(offer)
        if offer == self.preferences:
            self.offer = self.preferences
            return self.preferences

        opponents_offer = offer

        previous_offer = self.offer[:]

        # If we are on the last round, check if within -len(), else fail.
        # Or see offers that were within -len() traded previously.
        # if() If opponent made attempt to reconcile, take the offer.
        # print("curr iter is " + str(self.curr_num_iters))
        # print("iter lim is " + str(self.iter_limit - 1))

        if(self.i_went_first and self.curr_num_iters == self.iter_limit + 1):
            self.offer = offer[:]
            # print("i went first and this is my last round... the really last one, no pressure.")
            # print(self.max_opponent_util)
            # print(self.prev_opponent_util)
            # print((self.max_opponent_util - self.prev_opponent_util) / self.max_opponent_util)
            # print((self.my_max_util - self.utility()) / self.my_max_util )
            # print(self.my_max_util)
            # print(self.utility())
            if ((self.max_opponent_util - self.prev_opponent_util) / abs(self.max_opponent_util) > 0.8 *
                 (self.my_max_util - self.utility()) / abs(self.my_max_util) and self.utility() > -len(self.preferences) ):
                return offer
            else:
                self.offer = self.preferences[:]
                return self.preferences



        if(not self.i_went_first and self.curr_num_iters == self.iter_limit):
            # print("i went second and this is my last round, but is actually the second last round.")
            self.offer = offer[:]
            if ((self.max_opponent_util - self.prev_opponent_util) / abs(self.max_opponent_util) > 0.8 *
                 (self.my_max_util - self.utility()) / abs(self.my_max_util) and self.utility() > -len(self.preferences) ):
                return offer

        # First see if the opponent's offer is close enough to the curve
        our_util_given_opp_offer = self.get_custom_utility(self.preferences, opponents_offer)

        # Accept right away if offer higher than our curve.
        if(our_util_given_opp_offer >= self.sample_curve(self.curr_num_iters) * self.my_max_util):
            self.offer = offer
            return offer

        previous_utility = self.utility()

        # Otherwise Calculate the offer that will best fit the curve.
        if(((self.sample_curve(self.curr_num_iters) * self.my_max_util) - our_util_given_opp_offer) / (self.sample_curve(self.curr_num_iters) * self.my_max_util) > 0.2):
            # Respond with an offer that is with in this bound.
            bounding_value = 3000
            most_fit_offer = None
            most_fit_value = 1000000
            while bounding_value > 0:
                random.shuffle(opponents_offer)
                bounding_value -= 1

                our_util_given_opp_offer = self.get_custom_utility(self.preferences, opponents_offer)
                if(most_fit_value > ((self.sample_curve(self.curr_num_iters) * self.my_max_util) - our_util_given_opp_offer) / (self.sample_curve(self.curr_num_iters) * self.my_max_util)):
                    most_fit_value = ((self.sample_curve(self.curr_num_iters) * self.my_max_util) - our_util_given_opp_offer) / (self.sample_curve(self.curr_num_iters) * self.my_max_util)
                    most_fit_offer = opponents_offer[:]

            # print(our_util_given_opp_offer)
            self.offer = opponents_offer
            if(self.utility() > previous_utility):
                return opponents_offer
            else:
                self.offer = previous_offer
                return self.offer
        else:
            self.offer = opponents_offer
            return opponents_offer


    def get_custom_utility(self, custom_prefs, custom_offer):
        tmp_my_prefs = self.preferences[:]
        tmp_my_offer = self.offer[:]
        self.preferences = custom_prefs[:]
        self.offer = custom_offer[:]

        utility = self.utility()

        self.preferences = tmp_my_prefs
        self.offer = tmp_my_offer

        return utility

    def sample_curve(self, curr_num_iters):
        x = curr_num_iters / self.iter_limit * self.curve_len
        return (1-x*x)

    def swap_random(self, offer_to_sort):
        index1 = random.randint(0, len(offer_to_sort) - 1)
        index2 = random.randint(0, len(offer_to_sort) - 1)
        offer_to_sort[index1], offer_to_sort[index2] = offer_to_sort[index2], offer_to_sort[index1]

    # receive_utility(self : BaseNegotiator, utility : Float)
        # Store the utility the other negotiator received from their last offer
    def receive_utility(self, utility):
        if(self.max_opponent_util < utility):
            self.max_opponent_util = utility
        self.prev_opponent_util = utility

    # receive_results(self : BaseNegotiator, results : (Boolean, Float, Float, Int))
        # Store the results of the last series of negotiation (points won, success, etc.)
    def receive_results(self, results):
        self.initialize(self.preferences, self.iter_limit)