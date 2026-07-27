from src.load_data import load_decision_data


df = load_decision_data()
def clean_decisions(df):
    df = df.copy()

    df["match"] = df["match"].astype(str).str.strip().str.casefold()
    df["favored_team"] = df["favored_team"].astype(str).str.strip().str.casefold()
    df["underdog_team"] = df["underdog_team"].astype(str).str.strip().str.casefold()
    df["team_benefited"] = df["team_benefited"].astype(str).str.strip().str.casefold()
    df["team_hurt"] = df["team_hurt"].astype(str).str.strip().str.casefold()
    df["stage"] = df["stage"].astype(str).str.strip().str.upper()
    df["VAR_involved"] = df["VAR_involved"].astype(str).str.upper().str.strip().map({"TRUE": True, "FALSE": False})
    df["favored_team_benefited"] = df["favored_team_benefited"].astype(str).str.upper().str.strip().map({"TRUE": True, "FALSE": False})

    return df

def clean_context(mc):
    from src.load_data import load_match_context
    mc = load_match_context()
    mc = mc.copy()

    mc = mc.set_index("match_name")
    mc["winner"] = mc["winner"].astype(str).str.strip().str.casefold()

    return mc

