from pathlib import Path

import pandas as pd

def parse_count(
    value: object,
    source_file: Path,
    sheet_name: str,
    row_number: int,
    column_number: int,
) -> int:
    if pd.isna(value):
        raise ValueError(
            f"Missing value in {source_file}, "
            f"sheet {sheet_name}, "
            f"row {row_number}, "
            f"column {column_number}"
        )

    numeric_value = pd.to_numeric(value, errors="raise")

    if numeric_value < 0:
        raise ValueError(
            f"Negative value in {source_file}, "
            f"sheet {sheet_name}, "
            f"row {row_number}, "
            f"column {column_number}: {numeric_value}"
        )

    if numeric_value != int(numeric_value):
        raise ValueError(
            f"Expected an integer in {source_file}, "
            f"sheet {sheet_name}, "
            f"row {row_number}, "
            f"column {column_number}: {numeric_value}"
        )

    return int(numeric_value)
