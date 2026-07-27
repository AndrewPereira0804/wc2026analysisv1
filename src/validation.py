from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
MANUAL = ROOT / "data" / "manual"
PROCESSED = ROOT / "data" / "processed"

REQUIRED_DECISION_COLUMNS = [
    "incident_id",
    "match",
    "stage",
    "minute",
    "favored_team",
    "underdog_team",
    "team_benefited",
    "team_hurt",
    "incident_type",
    "decision",
    "favored_team_benefited",
    "score",
    "call_correctness",
    "confidence",
    "video_timestamp",
    "VAR_involved",
    "standard_fit",
    "notes",
]

REQUIRED_CONTEXT_COLUMNS = [
    "match_name",
    "stage",
    "favored_team",
    "underdog_team",
    "winner",
    "spread",
]


def validate_required_csv(path, required_columns, required_nonblank_columns=None):
    if required_nonblank_columns is None:
        required_nonblank_columns = required_columns

    if not path.exists():
        raise FileNotFoundError(f"Required file not found: {path}")

    if path.stat().st_size == 0:
        raise ValueError(f"Required file is empty: {path}")

    df = pd.read_csv(path)

    if df.empty:
        raise ValueError(f"Required file has headers but no rows: {path}")

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"{path.name} is missing required columns: {missing_columns}"
        )

    blank_columns = []
    for col in required_nonblank_columns:
        if df[col].isna().any() or (df[col].astype(str).str.strip() == "").any():
            blank_columns.append(col)

    if blank_columns:
        raise ValueError(
            f"{path.name} has blank required values in columns: {blank_columns}"
        )

    return df


def validate_manual_inputs():
    validate_required_csv(
        MANUAL / "decision.csv",
        REQUIRED_DECISION_COLUMNS,
        required_nonblank_columns=[
            "incident_id",
            "match",
            "stage",
            "minute",
            "favored_team",
            "underdog_team",
            "team_benefited",
            "team_hurt",
            "incident_type",
            "decision",
            "score",
            "call_correctness",
            "confidence",
            "VAR_involved",
            "standard_fit",
        ],
    )

    validate_required_csv(
        MANUAL / "match_context.csv",
        REQUIRED_CONTEXT_COLUMNS,
        required_nonblank_columns=[
            "match_name",
            "stage",
            "favored_team",
            "underdog_team",
            "winner",
            "spread",
        ],
    )

def assert_column_types(df, expected_types):

    type_checks = {
        "string": pd.api.types.is_string_dtype,
        "numeric": pd.api.types.is_numeric_dtype,
        "integer": pd.api.types.is_integer_dtype,
        "float": pd.api.types.is_float_dtype,
        "bool": pd.api.types.is_bool_dtype,
    }

    for column, expected_type in expected_types.items():
        assert column in df.columns, f"Missing column: {column}"

        if expected_type not in type_checks:
            raise ValueError(f"Unknown expected type: {expected_type}")

        actual_dtype = df[column].dtype
        check = type_checks[expected_type]

        assert check(df[column]), (
            f"Column '{column}' has wrong type. "
            f"Expected {expected_type}, got {actual_dtype}"
        )