import re
from datetime import date
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_FILENAME = "crimes_by_region.xls"

PERIOD_PATTERN = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")


def get_reporting_month(sheet_data: pd.DataFrame) -> date:
    for value in sheet_data.iloc[:10, 0].dropna():
        match = PERIOD_PATTERN.search(str(value))

        if match:
            _, month, year = map(int, match.groups())
            return date(year, month, 1)

    raise ValueError("Reporting period was not found in the sheet")


def find_header_row(sheet_data: pd.DataFrame) -> int:
    first_column = sheet_data.iloc[:, 0].astype(str).str.strip()
    matching_rows = sheet_data.index[first_column == "РЕГИОН"].tolist()

    if len(matching_rows) != 1:
        raise ValueError(
            f"Expected one REGION header, found {len(matching_rows)}"
        )

    return matching_rows[0]


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
    header_row = find_header_row(sheet_data)

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
            registered_crimes = sheet_data.iat[row_index, column_index]

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

    if len(crime_columns) != 9:
        raise ValueError(
            f"Expected 9 crime columns in {source_file}, "
            f"sheet {sheet_name}, found {len(crime_columns)}"
        )

    if len(result) != 270:
        raise ValueError(
            f"Expected 270 rows in {source_file}, "
            f"sheet {sheet_name}, found {len(result)}"
        )

    return result


def extract_crimes_by_region() -> pd.DataFrame:
    source_files = sorted(
        RAW_DATA_DIR.glob(f"*/{SOURCE_FILENAME}")
    )

    if len(source_files) != 3:
        raise FileNotFoundError(
            f"Expected 3 files named {SOURCE_FILENAME}, "
            f"found {len(source_files)}"
        )

    extracted_sheets = []

    for source_file in source_files:
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

    result = result.sort_values(
        by=[
            "reporting_month",
            "police_region_raw",
            "criminal_code_article_raw",
        ]
    ).reset_index(drop=True)

    return result


def main() -> None:
    data = extract_crimes_by_region()

    print(f"Rows extracted: {len(data)}")
    print(f"Reporting months: {data['reporting_month'].nunique()}")
    print(f"Source files: {data['source_file'].nunique()}")


if __name__ == "__main__":
    main()