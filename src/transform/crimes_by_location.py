from sqlalchemy import text
from src.common.database import get_engine


def transform_crimes_by_location(year: int) -> None:
    engine = get_engine()

    with engine.begin() as connection:
        invalid_rows_count = connection.execute(
            text("""
                select 
                    count(*)
                from 
                    staging.crimes_by_location cl
                    left join analytics.dim_date d_d on cl.reporting_month = d_d.calendar_date
                    left join analytics.dim_location_category d_lc on cl.location_type_raw = d_lc.location_category_name
                            and cl.location_breakdown_type = d_lc.classification_type        
                    left join analytics.crime_type_mapping ctm on ctm.source_crime_type_raw = cl.crime_type_raw
                    left join analytics.dim_crime_status d_cs on cl.crime_status = d_cs.crime_status_code
                where
                    d_d.calendar_date is null
                    or d_lc.location_category_id is null
                    or d_cs.crime_status_id is null       
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
                delete from analytics.fct_crimes_by_location where extract(year from reporting_month) = :year;
            """
            ),
            {"year": year}
        )

        connection.execute(
            text(
            """
                insert into analytics.fct_crimes_by_location
                (
                    reporting_month,
                    crime_type_id,
                    location_category_id,
                    crime_status_id,
                    crime_count,
                    datetime_created
                )
                select 
                    d_d.calendar_date,
                    ctm.crime_type_id,
                    d_lc.location_category_id,
                    d_cs.crime_status_id,
                    cl.crime_count,
                    now()                    
                from 
                    staging.crimes_by_location cl
                    inner join analytics.dim_date d_d on cl.reporting_month = d_d.calendar_date
                    inner join analytics.dim_location_category d_lc on cl.location_type_raw = d_lc.location_category_name
                            and cl.location_breakdown_type = d_lc.classification_type                        
                    inner join analytics.crime_type_mapping ctm on ctm.source_crime_type_raw = cl.crime_type_raw
                    inner join analytics.dim_crime_status d_cs on cl.crime_status = d_cs.crime_status_code
            """
            )
        )