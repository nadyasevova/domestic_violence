import re
from datetime import date

DATE_PATTERN = re.compile(r"(\d{2})\.(\d{2})\.(\d{4})")


def get_reporting_month(sheet_data: pd.DataFrame) -> date:
    for row_index in range(min(10, len(sheet_data))):
        for value in sheet_data.iloc[row_index].dropna():
            matches = DATE_PATTERN.findall(str(value))

            if matches:
                _, month, year = map(int, matches[-1])
                return date(year, month, 1)

    raise ValueError("Reporting period was not found in the sheet")


def find_header_row(sheet_data: pd.DataFrame, first_column_value: str) -> int:
    first_column = sheet_data.iloc[:, 0].astype(str).str.strip()

    matching_rows = sheet_data.index[
        first_column == first_column_value
    ].tolist()

    if len(matching_rows) != 1:
        raise ValueError(
            f"Expected one {first_column_value} header, "
            f"found {len(matching_rows)}"
        )

    return matching_rows[0]


