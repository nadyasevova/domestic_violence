import re
from datetime import date
from pathlib import Path

import pandas as pd

from src.common.data_validation import parse_count
from src.extract.common import get_reporting_month, find_header_row


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_FILENAME = "established_offenders.xls"


OFFENDER_CATEGORIES = {
    1: {
        "breakdown_type": "total",
        "offender_category_raw": "общ брой",
    },
    2: {
        "breakdown_type": "sex",
        "offender_category_raw": "жени",
    },
    3: {
        "breakdown_type": "age",
        "offender_category_raw": "под 14 години",
    },
    4: {
        "breakdown_type": "age",
        "offender_category_raw": "14–17 години",
    },
    5: {
        "breakdown_type": "age",
        "offender_category_raw": "18–30 години",
    },
    6: {
        "breakdown_type": "age",
        "offender_category_raw": "31–40 години",
    },
    7: {
        "breakdown_type": "age",
        "offender_category_raw": "над 40 години",
    },
}



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

    header_row = find_header_row(sheet_data, "Престъпления")

    records = []

    for row_index in range(header_row + 1, sheet_data.shape[0]):
        crime_type_value = sheet_data.iat[row_index, 0]

        if pd.isna(crime_type_value):
            continue

        crime_type = str(crime_type_value).strip()

        # Skip the row containing Excel column numbers: 1, 2, 3...
        if crime_type in {"1", "1.0"}:
            continue

        for column_index, category in OFFENDER_CATEGORIES.items():

            offender_count = parse_count(
                value=sheet_data.iat[row_index, column_index],
                source_file=source_file,
                sheet_name=sheet_name,
                row_number=row_index + 1,
                column_number=column_index + 1,
            )
        
            records.append(
                {
                    "reporting_month": reporting_month,
                    "crime_type_raw": crime_type,
                    "breakdown_type": category["breakdown_type"],
                    "offender_category_raw": category[
                        "offender_category_raw"
                    ],
                    "offender_count": offender_count,
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


def extract_established_offenders(year: int) -> pd.DataFrame:

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
