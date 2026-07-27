from src.load_data import load_cleaned_data


def get_match_incidents(title):
    title = title.strip().casefold()
    df = load_cleaned_data()
    match = df[df["match"] == title]
    if match.empty:
        return None
    return match


def get_incidents_by_team(team):
    team = team.strip().casefold()
    df = load_cleaned_data()
    return df[(df["favored_team"] == team) | (df["underdog_team"] == team)]
        
