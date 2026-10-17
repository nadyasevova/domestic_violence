from sqlalchemy import text
from src.common.database import get_engine


def transform_crimes_by_region(year: int) -> None:
    print ("Transforming crimes by region data...")

    engine = get_engine()

    with engine.begin() as connection:
        invalid_rows_count = connection.execute(
            text("""
                select 
                    count(*)
                from 
                    staging.crimes_by_region cr
                    left join analytics.dim_crime_type d_ct on cr.criminal_code_article_raw = d_ct.criminal_code_article
                    left join analytics.dim_police_structure d_ps on cr.police_region_raw = d_ps.police_structure_name
                    left join analytics.dim_date d_d on cr.reporting_month = d_d.calendar_date
                where
                    d_ct.crime_type_id is null
                    or d_ps.police_structure_id is null
                    or d_d.calendar_date is null;
            """
            )
        ).scalar_one()

        if invalid_rows_count > 0:
            raise ValueError(
                    f"Found {invalid_rows_count} invalid rows."
                )

        connection.execute(
            text("""
                delete from analytics.fct_crimes_by_region where extract(year from reporting_month) = :year;
            """
            ),
            {"year": year}
        )

        connection.execute(
            text(
            """
                insert into analytics.fct_crimes_by_region 
                (
                    reporting_month,
                    police_structure_id,
                    crime_type_id,
                    registered_crimes_count,
                    datetime_created
                )    
                select 
                    d_d.calendar_date,
                    d_ps.police_structure_id,
                    d_ct.crime_type_id,
                    cr.registered_crimes,
                    now()    
                from 
                    staging.crimes_by_region cr
                    inner join analytics.dim_crime_type d_ct on cr.criminal_code_article_raw = d_ct.criminal_code_article
                    inner join analytics.dim_police_structure d_ps on cr.police_region_raw = d_ps.police_structure_name
                    inner join analytics.dim_date d_d on cr.reporting_month = d_d.calendar_date;
            """
            )
        )