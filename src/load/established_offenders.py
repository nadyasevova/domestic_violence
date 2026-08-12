from sqlalchemy import text

from src.common.database import get_engine
from src.extract.established_offenders import extract_established_offenders

SCHEMA_NAME = "staging"
TABLE_NAME = "established_offenders"
CHUNK_SIZE = 1000


def load_established_offenders() -> None:
    data = extract_established_offenders()
    engine = get_engine()

    with engine.begin() as connection:
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

    print(f"Rows loaded: {loaded_rows}")
    print(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")


def main() -> None:
    load_established_offenders()


if __name__ == "__main__":
    main()