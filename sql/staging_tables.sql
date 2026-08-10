CREATE TABLE staging.crimes_by_region (
    staging_row_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    reporting_month DATE NOT NULL,
    police_region_raw VARCHAR(100) NOT NULL,
    criminal_code_article_raw VARCHAR(100) NOT NULL,
    registered_crimes INTEGER NOT NULL,
    source_file VARCHAR(255) NOT NULL,
    source_sheet VARCHAR(100) NOT NULL,
    source_row_number SMALLINT NOT NULL,
    source_column_number SMALLINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_registered_crimes_non_negative
        CHECK (registered_crimes >= 0)
);