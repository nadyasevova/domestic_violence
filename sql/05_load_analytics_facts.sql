truncate table analytics.fct_crimes_by_region;
insert into analytics.fct_crimes_by_region 
(
	reporting_month,
    police_structure_id,
    crime_type_id,
    registered_crimes_count
)    
select 
    d_d.calendar_date,
    d_ps.police_structure_id,
    d_ct.crime_type_id,
    cr.registered_crimes    
from 
	staging.crimes_by_region cr
    inner join analytics.dim_crime_type d_ct on cr.criminal_code_article_raw = d_ct.criminal_code_article
    inner join analytics.dim_police_structure d_ps on cr.police_region_raw = d_ps.police_structure_name
    inner join analytics.dim_date d_d on cr.reporting_month = d_d.calendar_date;




truncate table analytics.fct_crimes_by_location;
insert into analytics.fct_crimes_by_location
(
    reporting_month,
    crime_type_id,
	location_category_id,
	crime_status_id,
    crime_count
)
select 
	d_d.calendar_date,
	ctm.crime_type_id,
    d_lc.location_category_id,
    d_cs.crime_status_id,
    cl.crime_count
    
from 
	staging.crimes_by_location cl
    inner join analytics.dim_date d_d on cl.reporting_month = d_d.calendar_date
	inner join analytics.dim_location_category d_lc on cl.location_type_raw = d_lc.location_category_name
    		and cl.location_breakdown_type = d_lc.classification_type
        
    inner join analytics.crime_type_mapping ctm on ctm.source_crime_type_raw = cl.crime_type_raw
    inner join analytics.dim_crime_status d_cs on cl.crime_status = d_cs.crime_status_code
