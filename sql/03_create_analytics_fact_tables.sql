
drop table if exists analytics.fct_crimes_by_region;
create table analytics.fct_crimes_by_region (
    reporting_month date not null,
    police_structure_id smallint not null,
    crime_type_id smallint not null,
    registered_crimes_count smallint not null,

    primary key (reporting_month, police_structure_id, crime_type_id),

    foreign key (reporting_month) references analytics.dim_time (calendar_date),
    foreign key (police_structure_id) references analytics.dim_police_structure (police_structure_id),
    foreign key (crime_type_id) references analytics.dim_crime_type (crime_type_id),

    check (extract(day from reporting_month) = 1),
    check (registered_crimes_count >= 0)

);

