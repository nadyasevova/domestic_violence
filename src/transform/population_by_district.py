from sqlalchemy import text


def transform_population_by_district(year: int, connection: Connection) -> None:

    invalid_rows_count = connection.execute(
        text("""
            select 
                count(*)                   
            from 
                staging.established_offenders eo
                left join analytics.dim_date d_d on eo.reporting_month = d_d.calendar_date
                left join analytics.dim_offender_category d_oc on lower(eo.offender_category_raw) =  lower(d_oc.offender_category_name)
                left join analytics.crime_type_mapping ctm on ctm.source_crime_type_raw = eo.crime_type_raw
            where
                d_d.calendar_date is null
                or d_oc.offender_category_id is null
                or ctm.crime_type_id is null;
        """
        )
    ).scalar_one()

    if invalid_rows_count > 0:
        raise ValueError(
                f"Found {invalid_rows_count} invalid rows."
            )

    connection.execute(
        text("""
            delete from analytics.fct_established_offenders where extract(year from reporting_month) = :year;
        """
        ),
        {"year": year}
    )



    connection.execute(
        text(
        """
            insert into analytics.fct_established_offenders (
                reporting_month,
                crime_type_id,
                offender_category_id,
                established_offenders_count,
                datetime_created
            )
            select 
                d_d.calendar_date,
                ctm.crime_type_id,
                d_oc.offender_category_id,
                eo.offender_count,
                now()
            from 
                staging.established_offenders eo
                inner join analytics.dim_date d_d on eo.reporting_month = d_d.calendar_date
                inner join analytics.dim_offender_category d_oc on lower(eo.offender_category_raw) =  lower(d_oc.offender_category_name)
                inner join analytics.crime_type_mapping ctm on ctm.source_crime_type_raw = eo.crime_type_raw    
        """
        )
    )


    # print(f"Rows loaded: {invalid_rows_count}")
    # print(f"Target table: {SCHEMA_NAME}.{TABLE_NAME}")
