import numpy as np
from src.get_match import get_match_incidents

CORRECTNESS_EXPONENT = 1.5
STANDARD_FIT_BOOST = 0.5


def calculate_weighted_score(row):
    wrongness = 1 - row["call_correctness"]
    consistency_boost = 1 + STANDARD_FIT_BOOST * abs(row["standard_fit"])
    return (
        row["score"]
        * (wrongness ** CORRECTNESS_EXPONENT)
        * row["confidence"]
        * consistency_boost
    )

def calculate_abs_weighted_score(row):
    return abs(calculate_weighted_score(row))

def match_bias_score(title):
    match = get_match_incidents(title)
    if match is None or match.empty:
        return None
    else:
        weighted_scores = match.apply(calculate_weighted_score, axis=1)
        return np.round(weighted_scores.sum(), 2)
    
def abs_match_bias_score(title):
    match = get_match_incidents(title)
    if match is None or match.empty:
        return None
    else:
        weighted_scores = match.apply(calculate_abs_weighted_score, axis=1)
        return np.round(weighted_scores.sum(), 2)
