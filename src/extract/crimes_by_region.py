import re
from datetime import date
from pathlib import Path

import pandas as pd

from src.common.data_validation import parse_count
from src.extract.common import get_reporting_month, find_header_row

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_FILENAME = "crimes_by_region.xls"


def extract_sheet(
    workbook: pd.ExcelFile,
    sheet_name: str,
    source_file: Path,
) -> pd.DataFrame:
    sheet_data = pd.read_excel(
        workbook,
        sheet_name=sheet_name,
        header=None,
    )

    reporting_month = get_reporting_month(sheet_data)
    header_row = find_header_row(sheet_data, "РЕГИОН")

    crime_columns = []

    for column_index in range(1, sheet_data.shape[1]):
        header_value = sheet_data.iat[header_row, column_index]

        if pd.notna(header_value):
            crime_columns.append(
                (column_index, str(header_value).strip())
            )

    records = []

    for row_index in range(header_row + 1, sheet_data.shape[0]):
        region_value = sheet_data.iat[row_index, 0]

        if pd.isna(region_value):
            continue

        police_region = str(region_value).strip()

        # Skip the row containing Excel column numbers: 1, 2, 3...
        if police_region in {"1", "1.0"}:
            continue

        for column_index, criminal_code_article in crime_columns:
            registered_crimes = parse_count(
                value=sheet_data.iat[row_index, column_index],
                source_file=source_file,
                sheet_name=sheet_name,
                row_number=row_index + 1,
                column_number=column_index + 1,
            )

            if pd.isna(registered_crimes):
                raise ValueError(
                    f"Missing value in {source_file}, "
                    f"sheet {sheet_name}, "
                    f"row {row_index + 1}, "
                    f"column {column_index + 1}"
                )

            records.append(
                {
                    "reporting_month": reporting_month,
                    "police_region_raw": police_region,
                    "criminal_code_article_raw": criminal_code_article,
                    "registered_crimes": int(registered_crimes),
                    "source_file": str(
                        source_file.relative_to(RAW_DATA_DIR)
                    ),
                    "source_sheet": sheet_name,
                    "source_row_number": row_index + 1,
                    "source_column_number": column_index + 1,
                }
            )

    result = pd.DataFrame(records)

    return result


def extract_crimes_by_region(year: int) -> pd.DataFrame:

    source_file = RAW_DATA_DIR / str(year) / SOURCE_FILENAME

    if not source_file.exists():
        raise FileNotFoundError(
            f"Expected file {source_file} does not exist"
        )

    extracted_sheets = []
    with pd.ExcelFile(source_file, engine="xlrd") as workbook:
        for sheet_name in workbook.sheet_names:
            extracted_sheets.append(
                extract_sheet(
                    workbook=workbook,
                    sheet_name=sheet_name,
                    source_file=source_file,
                )
            )

    result = pd.concat(extracted_sheets, ignore_index=True)

    return result