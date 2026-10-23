
drop table if exists analytics.fct_crimes_by_region;
create table analytics.fct_crimes_by_region (
    reporting_month date not null,
    police_structure_id smallint not null,
    crime_type_id smallint not null,
    registered_crimes_count smallint not null,
    datetime_created timestamp not null default now(),

    primary key (reporting_month, police_structure_id, crime_type_id),

    foreign key (reporting_month) references analytics.dim_date (calendar_date),
    foreign key (police_structure_id) references analytics.dim_police_structure (police_structure_id),
    foreign key (crime_type_id) references analytics.dim_crime_type (crime_type_id),

    check (extract(day from reporting_month) = 1),
    check (registered_crimes_count >= 0)

);


drop table if exists analytics.fct_crimes_by_location;
create table analytics.fct_crimes_by_location (

    reporting_month date not null,
    crime_type_id smallint not null,
	location_category_id smallint not null,
	crime_status_id smallint not null,
    
    crime_count smallint not null,
    datetime_created timestamp not null default now(),

    primary key (reporting_month, crime_type_id, location_category_id, crime_status_id),

    foreign key (reporting_month) references analytics.dim_date (calendar_date),
    foreign key (location_category_id) references analytics.dim_location_category (location_category_id),
    foreign key (crime_type_id) references analytics.dim_crime_type (crime_type_id),
    foreign key (crime_status_id) references analytics.dim_crime_status (crime_status_id),

    check (extract(day from reporting_month) = 1),
    check (crime_count >= 0)
);


drop table if exists analytics.fct_established_offenders;
create table analytics.fct_established_offenders (

    reporting_month date not null,
    crime_type_id smallint not null,
	offender_category_id smallint not null,

    established_offenders_count smallint not null,
    datetime_created timestamp not null default now(),

    primary key (reporting_month, crime_type_id, offender_category_id),

    foreign key (reporting_month) references analytics.dim_date (calendar_date),
    foreign key (crime_type_id) references analytics.dim_crime_type (crime_type_id),
    foreign key (offender_category_id) references analytics.dim_offender_category (offender_category_id),

    check (extract(day from reporting_month) = 1),
    check (established_offenders_count >= 0)
);


drop table if exists analytics.fct_population_by_district;
create table analytics.fct_population_by_district (

    population_date date not null,
    district_id smallint not null,
	population_total_count integer not null,
	population_men integer not null,
	population_women integer not null,

    primary key (population_date, district_id),

    foreign key (population_date) references analytics.dim_date (calendar_date),
    foreign key (district_id) references analytics.dim_district (district_id),

    check (population_total_count >= 0),
    check (population_men >= 0),
    check (population_women >= 0),
    check (population_total_count = population_men + population_women)
);