from pathlib import Path

import pandas as pd

from src.common.data_validation import parse_count
from src.extract.common import get_reporting_month, find_header_row


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_FILENAME = "crimes_by_location.xls"

LOCATION_COLUMNS = {
    1: {
        "location_breakdown_type": "public_place",
        "location_type_raw": "Обществени места",
        "crime_status": "registered",
    },
    2: {
        "location_breakdown_type": "public_place",
        "location_type_raw": "Обществени места",
        "crime_status": "solved",
    },
    3: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Регионален център",
        "crime_status": "registered",
    },
    4: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Регионален център",
        "crime_status": "solved",
    },
    5: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Град",
        "crime_status": "registered",
    },
    6: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Град",
        "crime_status": "solved",
    },
    7: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Село",
        "crime_status": "registered",
    },
    8: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Село",
        "crime_status": "solved",
    },
    9: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Извън населено място",
        "crime_status": "registered",
    },
    10: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Извън населено място",
        "crime_status": "solved",
    },
    11: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Вилна зона",
        "crime_status": "registered",
    },
    12: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Вилна зона",
        "crime_status": "solved",
    },
    13: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Гранична зона",
        "crime_status": "registered",
    },
    14: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "Гранична зона",
        "crime_status": "solved",
    },
    15: {
        "location_breakdown_type": "geographic_area", 
        "location_type_raw": "ГКПП",
        "crime_status": "registered",
    },
    16: {
        "location_breakdown_type": "geographic_area",
        "location_type_raw": "ГКПП",
        "crime_status": "solved",
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

        # Skip the technical row containing Excel column numbers.
        if crime_type in {"1", "1.0"}:
            continue

        for column_index, column_metadata in LOCATION_COLUMNS.items():
            crime_count = parse_count(
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
                    "location_breakdown_type": column_metadata[
                        "location_breakdown_type"
                    ],
                    "location_type_raw": column_metadata[
                        "location_type_raw"
                    ],
                    "crime_status": column_metadata["crime_status"],
                    "crime_count": crime_count,
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


def extract_crimes_by_location(year: int) -> pd.DataFrame:
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

    result = pd.concat(
        extracted_sheets,
        ignore_index=True,
    )

    return result
