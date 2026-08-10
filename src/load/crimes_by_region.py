from sqlalchemy import text

from src.common.database import get_engine
from src.extract.crimes_by_region import extract_crimes_by_region

SCHEMA_NAME = "staging"
TABLE_NAME = "crimes_by_region"
CHUNK_SIZE = 1000


def load_crimes_by_region() -> None:
    data = extract_crimes_by_region()
    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE staging.crimes_by_region "
                "RESTART IDENTITY"
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
            text("SELECT COUNT(*) FROM staging.crimes_by_region")
        ).scalar_one()

        if loaded_rows != len(data):
            raise RuntimeError(
                f"Expected {len(data)} rows, loaded {loaded_rows}"
            )

    print(f"Rows loaded: {loaded_rows}")
    print(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")


def main() -> None:
    load_crimes_by_region()


if __name__ == "__main__":
    main()