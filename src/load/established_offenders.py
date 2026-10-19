import logging
from sqlalchemy import text

from src.extract.established_offenders import extract_established_offenders

SCHEMA_NAME = "staging"
TABLE_NAME = "established_offenders"
CHUNK_SIZE = 1000

logger = logging.getLogger(__name__)

def load_established_offenders(year: int, connection: Connection) -> None:

    data = extract_established_offenders(year)

    connection.execute(
        text(
            "truncate table staging.established_offenders "
            "restart identity"
        )
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
        text("select count(*) from staging.established_offenders")
    ).scalar_one()

    if loaded_rows != len(data):
        raise RuntimeError(
            f"Expected {len(data)} rows, loaded {loaded_rows}"
        )

    logger.info(f"Rows loaded: {loaded_rows}")
    logger.info(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")
