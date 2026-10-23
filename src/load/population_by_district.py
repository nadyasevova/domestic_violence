import logging
from sqlalchemy import text

from src.common.logging_config import init_logging
from src.common.database import get_engine
from src.extract.population_by_district import extract_population_by_district
from src.transform.population_by_district import transform_population_by_district

SCHEMA_NAME = "staging"
TABLE_NAME = "population_by_district"
CHUNK_SIZE = 1000

logger = logging.getLogger(__name__)
init_logging()

def load_population_by_district(year: int, connection: Connection) -> None:
    logger.info(f"starting to load population by district for year {year}")

    data = extract_population_by_district(year, connection)

    connection.execute(
            text("delete from staging.population_by_district where extract(year from population_date) = :year"),
            {"year": year}
        )

    data.to_sql(
        name=TABLE_NAME,
        schema=SCHEMA_NAME,
        con=connection,
        if_exists="append",
        index=False,
        chunksize=CHUNK_SIZE,
        method="multi",
    )

    loaded_rows = connection.execute(
        text("select count(*) from staging.population_by_district where extract(year from population_date) = :year"),
        {"year": year}
    ).scalar_one()


    if loaded_rows != len(data):
        raise RuntimeError(
            f"Expected {len(data)} rows, loaded {loaded_rows}"
        )

    logger.info(f"Rows loaded: {loaded_rows}")
    logger.info(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")



engine = get_engine()
with engine.begin() as connection:
    load_population_by_district(2025, connection)

    logger.info(f"Start transforming population by district for year 2025")
    transform_population_by_district(2025, connection)
    logger.info(f"End transforming population by district for year 2025")
