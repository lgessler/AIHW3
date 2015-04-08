from negotiator_framework import negotiate,read_scenario
from itertools import combinations
import os

from naive_negotiator import NaiveNegotiator
from negotiator import Negotiator
from test_negotiators import Selfish_Negotiator, Mostly_Selfish_Negotiator

negotiators = [
    NaiveNegotiator(),
    Negotiator(),
    Selfish_Negotiator(),
    Mostly_Selfish_Negotiator(),
]

performance = {x : 0 for x in negotiators}
csvs = [os.path.join('test_cases',x) for x in os.listdir('test_cases')]


def round_of_ten(negotiator_a, negotiator_b):
    score_a = score_b = 0
    for scenario in csvs:
        # Get the scenario parameters
        (num_iters, mapping) = read_scenario(scenario)
        # Separate the mapping out for each negotiator, and sort the items from it into a list
        # based upon the preferences of each negotiator
        a_mapping = {item["item_name"] : int(item["negotiator_a"]) for item in mapping}
        a_order = sorted(a_mapping, key=a_mapping.get, reverse=True)
        b_mapping = {item["item_name"] : int(item["negotiator_b"]) for item in mapping}
        b_order = sorted(b_mapping, key=b_mapping.get, reverse=True)
        # Give each negotiator their preferred item ordering
        negotiator_a.initialize(a_order, num_iters)
        negotiator_b.initialize(b_order, num_iters)
        # Get the result of the negotiation
        (result, order, count) = negotiate(num_iters, negotiator_a, negotiator_b)
        # Assign points to each negotiator. Note that if the negotiation failed, each negotiatior receives a negative penalty
        # However, it is also possible in a "successful" negotiation for a given negotiator to receive negative points
        (points_a, points_b) = (negotiator_a.utility(), negotiator_b.utility()) if result else (-len(a_order), -len(b_order))
        results = (result, points_a, points_b, count)
        score_a += points_a
        score_b += points_b
        # Update each negotiator with the final result, points assigned, and number of iterations taken to reach an agreement
        negotiator_a.receive_results(results)
        negotiator_b.receive_results(results)
        print("{} negotiation:\n\tNegotiator A: {}\n\tNegotiator B: {}".format("Successful" if result else "Failed", points_a, points_b))
    print("Final result:\n\tNegotiator A: {}\n\tNegotiator B: {}".format(score_a, score_b))
    return score_a,score_b


for a,b in combinations(negotiators, 2):
    sa, sb = round_of_ten(a,b)
    performance[a] += sa
    performance[b] += sb

for neg,score in performance.items():
    print neg.__class__.__name__,score
