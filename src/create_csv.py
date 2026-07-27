from pathlib import Path
import sys

import numpy as np
import pandas as pd

from src.aggregate import team_impact
from src.cleaning import clean_context, clean_decisions
from src.load_data import (
    load_cleaned_data,
    load_decision_data,
    load_match_context,
    load_match_sheet,
)
from src.scores import calculate_abs_weighted_score, abs_match_bias_score, match_bias_score
from src.validation import validate_manual_inputs

root = Path(__file__).resolve().parents[1]

if str(root) not in sys.path:
    sys.path.append(str(root))

def create_cleaned():
    df = load_decision_data()
    df = clean_decisions(df)
    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    df = df.set_index("incident_id")
    df.to_csv(processed / "cleaned.csv", index=True)

def create_team_sheet():
    team_sheet = pd.DataFrame()
    df = load_cleaned_data()
    team_sheet["team"] = pd.concat([df["favored_team"], df["underdog_team"]], ignore_index=True).drop_duplicates().reset_index(drop=True)

    matches_played = (
        pd.concat([
            df[["favored_team", "match"]].rename(columns={"favored_team": "team"}),
            df[["underdog_team", "match"]].rename(columns={"underdog_team": "team"}),
        ], ignore_index=True)
        .drop_duplicates()
        .groupby("team")["match"]
        .count()
        .sort_values(ascending=False)
    )

    team_sheet["matches_played"] = matches_played.reindex(team_sheet["team"]).values
    incident_counts = pd.concat([
    df["favored_team"],
    df["underdog_team"]
    ]).value_counts()

    team_sheet["incident_count"] = team_sheet["team"].map(incident_counts).fillna(0).astype(int)
    team_sheet["impact"] = team_sheet["team"].astype(str).apply(team_impact)
    team_sheet["impact_per_match"] = (
        team_sheet["impact"] / team_sheet["matches_played"]
    ).round(2)
    team_sheet = team_sheet.set_index("team")


    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    team_sheet.to_csv(processed / "team_sheet.csv", index=True)

def create_match_sheet():
    match_table = pd.DataFrame()
    df = load_cleaned_data()
    mc = load_match_context()
    mc = clean_context(mc)

    match_table["match_name"] = mc.index
    match_table["match_bias_score"] = match_table["match_name"].apply(match_bias_score)
    match_table["abs_bias_significance"] = match_table["match_name"].apply(abs_match_bias_score)

    incident_counts = df["match"].value_counts()
    match_stage = df.groupby("match")["stage"].first()
    match_table["stage"] = match_table["match_name"].map(match_stage)
    match_table["incident_count"] = match_table["match_name"].map(incident_counts)
    match_table = match_table.set_index("match_name")

    match_table["favored_team"] = mc["favored_team"]
    match_table["underdog_team"] = mc["underdog_team"]
    match_table["winner"] = mc["winner"]
    match_table["spread"] = mc["spread"]

    match_table["upset"] = match_table["winner"] == mc["underdog_team"]
    match_table["bias_direction"] = match_table["match_bias_score"].apply(
        lambda score: "favorite" if score > 0.75
        else "underdog" if score < -0.75
        else "neutral"
    )
    match_table["VAR_count"] = df.groupby("match")["VAR_involved"].sum()
    


    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    match_table.to_csv(processed / "match_sheet.csv", index=True)

def create_match_context():
    df = load_cleaned_data()
    match_context = pd.DataFrame()

    match_context["match_name"] = (
        df["match"]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    stage_by_match = df.groupby("match", sort=False)["stage"].first()
    favored_team_by_match = df.groupby("match", sort=False)["favored_team"].first()
    underdog_team_by_match = df.groupby("match", sort=False)["underdog_team"].first()
    match_context["stage"] = match_context["match_name"].map(stage_by_match)
    match_context["favored_team"] = match_context["match_name"].map(favored_team_by_match)
    match_context["underdog_team"] = match_context["match_name"].map(underdog_team_by_match)
    match_context["winner"] = None
    match_context["spread"] = None
    manual = root / "data" / "manual"
    manual.mkdir(parents=True, exist_ok=True)
    output_path = manual / "match_context.csv"

    if output_path.exists():
        raise FileExistsError("match_context.csv already exists. Verify existing info is correct and consistent with logged incidents, or delete the file and start over.")
    match_context.to_csv(manual / "match_context.csv", index=False)

def create_processed_incidents():
    incidents = pd.DataFrame()
    df = load_cleaned_data()
    df = df.set_index("incident_id")
    incidents["incident_id"] = df.index
    incidents = incidents.set_index("incident_id")
    incidents["favored_team_hurt"] = df["team_hurt"] == df["favored_team"]
    incidents["underdog_team_benefited"] = df["team_benefited"] == df["underdog_team"]
    incidents["abs_bias_significance"] = df.apply(calculate_abs_weighted_score, axis=1)
    incidents["incident_type"] = df["incident_type"].astype(str).str.strip()
    incidents["decision"] = df["decision"].astype(str).str.strip()
    incidents["unfairness_bucket"] = pd.cut(
        df.apply(calculate_abs_weighted_score, axis=1),
        bins=[0, 0.25, 0.5, 1, 1.75, 100],
        labels=["Probably fair", "Questionable", "Minorly unfair", "Unfair", "robbery"],
        include_lowest=True
    )

    incidents["VAR_involved"] = df["VAR_involved"]

    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    incidents.to_csv(processed / "processed_incidents.csv", index=True)

def create_stage_sheet():
    stage_sheet = pd.DataFrame()
    df = load_cleaned_data()
    ms = load_match_sheet()
    stage_sheet["stage"] = ["R32", "R16", "QF", "SF", "3P", "F"]
    match_num = ms.groupby("stage")["match_name"].count()
    stage_sheet["logged_matches"] = stage_sheet["stage"].map(match_num).fillna(0).astype(int)
    incidents_by_stage = df.groupby("stage")["incident_id"].count()
    stage_sheet["incidents"] = stage_sheet["stage"].map(incidents_by_stage).fillna(0).astype(int)
    stage_sheet["incidents_per_stage"] = stage_sheet["incidents"] / stage_sheet["logged_matches"]
    stage_abs_bias_significance = ms.groupby("stage")["abs_bias_significance"].sum()
    stage_score = ms.groupby("stage")["match_bias_score"].sum()
    stage_sheet["abs_total_match_bias_score"] = stage_sheet["stage"].map(stage_abs_bias_significance).fillna(0)
    stage_sheet["total_match_bias_score"] = stage_sheet["stage"].map(stage_score).fillna(0)
    stage_sheet["abs_bias_significance_per_match"] = np.round(stage_sheet["abs_total_match_bias_score"] / stage_sheet["logged_matches"], 2)
    stage_sheet["score_per_match"] = np.round(stage_sheet["total_match_bias_score"] / stage_sheet["logged_matches"], 2)


    processed = root / "data" / "processed"
    processed.mkdir(parents=True, exist_ok=True)
    stage_sheet.to_csv(processed / "stage_sheet.csv", index=False)


def create_all_processed():
    validate_manual_inputs()

    create_cleaned()
    create_processed_incidents()
    create_match_sheet()
    create_team_sheet()
    create_stage_sheet()
