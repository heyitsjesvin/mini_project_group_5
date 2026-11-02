"""Helpers shared by pipeline.py, check_member.py and the tests."""
import importlib

MEMBER_MODULES = {
    1: "etl.member1_extract_and_structure",
    2: "etl.member2_missing_values",
    3: "etl.member3_invalid_and_outliers",
    4: "etl.member4_features",
    5: "etl.member5_reports_and_load",
}

# Function that each member's module must provide for the transform stages
STAGE_FUNCTIONS = {
    1: "structural_cleaning",
    2: "handle_missing_values",
    3: "remove_invalid_and_outliers",
    4: "add_features",
}


def load_member_module(number):
    return importlib.import_module(MEMBER_MODULES[number])


def is_stub(number):
    """True while a member's file is still the placeholder."""
    return getattr(load_member_module(number), "IS_STUB", False)


def run_stages(df, upto):
    """Apply transform stages 1..upto (max 4) to a DataFrame."""
    for number in range(1, min(upto, 4) + 1):
        stage = getattr(load_member_module(number), STAGE_FUNCTIONS[number])
        df = stage(df)
    return df
