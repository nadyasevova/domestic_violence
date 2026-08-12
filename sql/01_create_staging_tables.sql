create schema if not exists staging;

drop table if exists staging.crimes_by_location cascade;
drop table if exists staging.crimes_by_region cascade;
drop table if exists staging.established_offenders cascade;

create table if not exists staging.crimes_by_region (
    staging_row_id integer generated always as identity primary key,

    reporting_month date not null,
    police_region_raw varchar(100) not null,
    criminal_code_article_raw varchar(100) not null,
    registered_crimes integer not null,

    source_file varchar(255) not null,
    source_sheet varchar(100) not null,
    source_row_number smallint not null,
    source_column_number smallint not null,

    loaded_at timestamptz not null default CURRENT_TIMESTAMP,

    constraint chk_registered_crimes_non_negative check (registered_crimes >= 0),
    constraint chk_source_row_number_positive check (source_row_number > 0),
    constraint chk_source_column_number_positive check (source_column_number > 0)
);


create table if not exists staging.established_offenders (
    staging_row_id integer generated always as identity primary key,

    reporting_month date not null,
    crime_type_raw varchar(100) not null,

    breakdown_type varchar(20) not null,
    offender_category_raw varchar(100) not null,
    offender_count smallint not null,

    source_file varchar(255) not null,
    source_sheet varchar(100) not null,
    source_row_number smallint not null,
    source_column_number smallint not null,

    loaded_at timestamptz not null default current_timestamp,

    constraint chk_offender_count_non_negative check (offender_count >= 0),
    constraint chk_offender_breakdown_type check (breakdown_type in ('total', 'sex', 'age')),
    constraint chk_offender_source_position_positive
        check (
            source_row_number > 0
            and source_column_number > 0
        )
);


create table if not exists staging.crimes_by_location (
    staging_row_id integer generated always as identity primary key,

    reporting_month date not null,
    crime_type_raw varchar(100) not null,

    location_breakdown_type varchar(30) not null,
    location_type_raw varchar(100) not null,

    crime_status varchar(20) not null,
    crime_count smallint not null,

    source_file varchar(255) not null,
    source_sheet varchar(100) not null,
    source_row_number smallint not null,
    source_column_number smallint not null,

    loaded_at timestamptz not null default current_timestamp,

    constraint chk_crime_count_non_negative check (crime_count >= 0),
    constraint chk_location_breakdown_type check (
            location_breakdown_type in (
                'public_place',
                'location_type'
            )
        ),
    constraint chk_crime_status check (
            crime_status in (
                'registered',
                'solved'
            )
        ),

    constraint chk_crimes_by_location_source_position_positive
        check (
            source_row_number > 0
            and source_column_number > 0
        )
);