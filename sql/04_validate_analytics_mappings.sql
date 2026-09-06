/*
    Validate there are no missing values when joining stagin raw table with dim tables
*/

select 
    cr.reporting_month,
    cr.police_region_raw,
    cr.registered_crimes,
	cr.criminal_code_article_raw,
    d_ct.crime_type_id,
	d_ps.police_structure_id,
	d_d.calendar_date
    
from 
	staging.crimes_by_region cr
    left join analytics.dim_crime_type d_ct on cr.criminal_code_article_raw = d_ct.criminal_code_article
    left join analytics.dim_police_structure d_ps on cr.police_region_raw = d_ps.police_structure_name
    left join analytics.dim_date d_d on cr.reporting_month = d_d.calendar_date
where
	d_ct.crime_type_id is null
    or d_ps.police_structure_id is null
    or d_d.calendar_date is null





select 
    cl.reporting_month,
    cl.crime_type_raw,
	cl.crime_status,
    cl.location_type_raw,
    cl.location_breakdown_type,
    
	d_d.calendar_date,
    d_lc.location_category_id,

	ctm.crime_type_id,
    d_cs.crime_status_id,
    cl.crime_count
    
    
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
    
    or ctm.crime_type_id is null        