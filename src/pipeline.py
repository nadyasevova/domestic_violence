import argparse
from pathlib import Path

from src.load.crimes_by_region import load_crimes_by_region
from src.load.crimes_by_location import load_crimes_by_location
from src.load.established_offenders import load_established_offenders

from src.transform.crimes_by_region import transform_crimes_by_region
from src.transform.crimes_by_location import transform_crimes_by_location
from src.transform.established_offenders import transform_established_offenders

RAW_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"

def main() -> None:
    parser = argparse.ArgumentParser(description="Extract data from established offenders Excel file.")

    parser.add_argument(
        "--year",
        type=int,
        default=None,
        help="Year to process. If omitted, process all available years.",
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        choices=[
            "established_offenders", 
            "crimes_by_region", 
            "crimes_by_location"
        ],
        help="Dataset to process.",
    )

    args = parser.parse_args()

    if args.year is None:
        years = []
        for source_file in RAW_DATA_DIR.glob(
            f"*/{args.dataset}.xls"
        ):
            if source_file.is_file() and source_file.parent.name.isdigit():
                years.append(int(source_file.parent.name))

        if not years:
            parser.error(
                f"No source files found for {args.dataset}."
            )

        years.sort()
    else:
        source_file = (
            RAW_DATA_DIR
            / str(args.year)
            / f"{args.dataset}.xls"
        )

        if not source_file.is_file():
            parser.error(f"Source file not found: {source_file}")

        years = [args.year]


    dataset_steps = {
        "established_offenders": (load_established_offenders, transform_established_offenders),
        "crimes_by_region": (load_crimes_by_region, transform_crimes_by_region),
        "crimes_by_location": (load_crimes_by_location, transform_crimes_by_location)
    }

    load_data, transform_data = dataset_steps[args.dataset]
    for year in years:
        print(f"Processing year: {year}")
        load_data(year=year)
        transform_data(year=year)

if __name__ == "__main__":
    main()