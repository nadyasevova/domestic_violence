import argparse
import logging

from pathlib import Path

from src.common.database import get_engine
from src.common.logging_config import init_logging

from src.load.crimes_by_region import load_crimes_by_region
from src.load.crimes_by_location import load_crimes_by_location
from src.load.established_offenders import load_established_offenders

from src.transform.crimes_by_region import transform_crimes_by_region
from src.transform.crimes_by_location import transform_crimes_by_location
from src.transform.established_offenders import transform_established_offenders

RAW_DATA_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
LOGGING_DIR = Path(__file__).resolve().parents[1] / "logs"


def main() -> None:
    
    logger = logging.getLogger(__name__)
    init_logging()

    logger.info("Starting data extraction and transformation pipeline.")

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
    
    logger.info(f"Arguments: {args}")

    if args.year is None:
        years = []
        for source_file in RAW_DATA_DIR.glob(
            f"*/{args.dataset}.xls"
        ):
            if source_file.is_file() and source_file.parent.name.isdigit():
                years.append(int(source_file.parent.name))

        if not years:
            message = f"No source files found for {args.dataset}."
            parser.error(message)

        years.sort()
    else:
        source_file = (
            RAW_DATA_DIR
            / str(args.year)
            / f"{args.dataset}.xls"
        )

        if not source_file.is_file():
            message = f"Source file not found: {source_file}"
            logger.error(message)
            parser.error(message)

        years = [args.year]


    dataset_steps = {
        "established_offenders": (load_established_offenders, transform_established_offenders),
        "crimes_by_region": (load_crimes_by_region, transform_crimes_by_region),
        "crimes_by_location": (load_crimes_by_location, transform_crimes_by_location)
    }

    load_data, transform_data = dataset_steps[args.dataset]

    logger.info(
        "Processing started: dataset=%s",
        args.dataset
    )

    engine = get_engine()
    try:
        for year in years:

            with engine.begin() as connection:
                logger.info("Year=%s",year)
                
                logger.info("Loading data started")
                load_data(year=year, connection=connection)
                logger.info("Loading data completed")


                logger.info("Transforming data started")
                transform_data(year=year, connection=connection)
                logger.info("Transforming data completed")

    except Exception:
        logger.exception(
            "Processing failed: dataset=%s year=%s",
            args.dataset,
            year,
        )
        raise
    else:
        logger.info(
            "Processing completed successfully: dataset=%s years=%s",
            args.dataset,
            years,
        )


if __name__ == "__main__":
    main()