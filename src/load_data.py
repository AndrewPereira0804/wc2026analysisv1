from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "data" / "manual"
PROCESSED = ROOT / "data" / "processed"


def load_decision_data():
    return pd.read_csv(MANUAL / "decision.csv", comment="#")


def load_match_context():
    return pd.read_csv(MANUAL / "match_context.csv")


def load_cleaned_data():
    return pd.read_csv(PROCESSED / "cleaned.csv")


def load_match_sheet():
    return pd.read_csv(PROCESSED / "match_sheet.csv")


def load_team_sheet():
    return pd.read_csv(PROCESSED / "team_sheet.csv")


def load_incidents():
    return pd.read_csv(PROCESSED / "processed_incidents.csv")


def load_stage_sheet():
    return pd.read_csv(PROCESSED / "stage_sheet.csv")

