import numpy as np

from src.get_match import get_incidents_by_team
from src.scores import calculate_weighted_score


#total of weighted benefit - weighted hurt a team experienced
#positive suggests they saw overall benefit from calls, negative suggests they were overall hurt by calls
def team_impact(team):
    total = 0
    team = team.strip().casefold()
    df = get_incidents_by_team(team)
    x = df[df["favored_team"] == team]
    total += x.apply(calculate_weighted_score, axis=1).sum()
    x = df[df["underdog_team"] == team]
    total -= x.apply(calculate_weighted_score, axis=1).sum()
    return np.round(total, 2)
