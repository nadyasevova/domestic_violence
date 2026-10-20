import logging
from sqlalchemy import text

from src.common.database import get_engine
from src.extract.crimes_by_region import extract_crimes_by_region

SCHEMA_NAME = "staging"
TABLE_NAME = "crimes_by_region"
CHUNK_SIZE = 1000

logger = logging.getLogger(__name__)
def load_crimes_by_region(year: int, connection: Connection) -> None:
    data = extract_crimes_by_region(year=year)

    connection.execute(
            text("delete from staging.crimes_by_region where extract(year from reporting_month) = :year"),
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
        text("select count(*) from staging.crimes_by_region where extract(year from reporting_month) = :year"),
        {"year": year}
    ).scalar_one()

    if loaded_rows != len(data):
        raise RuntimeError(
            f"Expected {len(data)} rows, loaded {loaded_rows}"
        )

    logger.info(f"Rows loaded: {loaded_rows}")
    logger.info(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")
