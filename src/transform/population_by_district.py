from sqlalchemy import text


def transform_population_by_district(year: int, connection: Connection) -> None:

    invalid_rows_count = connection.execute(
        text("""
            select
                count(*)
            from
                staging.population_by_district pd
                left join analytics.dim_date ddate on ddate.calendar_date = pd.population_date
                left join analytics.dim_district dd on dd.district_name = 
                    case pd.district_name_raw
                        when 'София (столица)' then 'София-град'
                        when 'София' then 'София-област'
                        else pd.district_name_raw
                    end    
                
            where 
                (dd.district_id is null
                or ddate.calendar_date is null)
	            and extract (year from pd.population_date) = :year
            """
        ),
        {"year": year}
    ).scalar_one()

    if invalid_rows_count > 0:
        raise ValueError(
            f"Found {invalid_rows_count} population rows "
            f"with missing district or date mappings for {year}."
        )

    connection.execute(
        text("""
            delete from analytics.fct_population_by_district where extract(year from population_date) = :year;
        """
        ),
        {"year": year}
    )

    connection.execute(
        text(
        """
            insert into analytics.fct_population_by_district (
                population_date,
                district_id,
                population_total_count,
                population_men,
                population_women
            )

            select
                ddate.calendar_date,
                dd.district_id,
                pd.population_total_count,
                pd.population_men,
                pd.population_women
            from
                staging.population_by_district pd
                inner join analytics.dim_date ddate on ddate.calendar_date = pd.population_date
                inner join analytics.dim_district dd on dd.district_name = 
                    case pd.district_name_raw
                        when 'София (столица)' then 'София-град'
                        when 'София' then 'София-област'
                        else pd.district_name_raw
                    end 
            where
                extract (year from pd.population_date) = :year
        """
        ),
        {"year": year}
    )