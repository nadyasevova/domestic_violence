create schema if not exists analytics;


drop table if exists analytics.dim_crime_type cascade;
create table if not exists analytics.dim_crime_type (
    crime_type_id smallint primary key,
    crime_type_name varchar(100) not null,
    criminal_code_article varchar(100) not null,
    display_order smallint not null,

    constraint uq_crime_type_name unique (crime_type_name),
    constraint uq_criminal_code_article unique (criminal_code_article),
    constraint uq_crime_type_display_order unique (display_order),
    constraint chk_crime_type_display_order_positive check (display_order > 0)
);

insert into analytics.dim_crime_type 
    (crime_type_id, crime_type_name, criminal_code_article, display_order)
values
    (1, 'Убийство', 'чл.116, ал.1, т.6а', 1),
    (2, 'Телесна повреда', 'чл.131, ал.1, т.5а', 2),
    (3, 'Отвличане', 'чл.142, ал.2, т.5а', 3),
    (4, 'Лишаване от свобода', 'чл.142а, ал.4', 4),
    (5, 'Принуда', 'чл.143, ал.3, т.1', 5),
    (6, 'Закана', 'чл.144, ал.3, т.3', 6),
    (7, 'Следене', 'чл.144а, ал.3', 7),
    (8, 'Неизпълнение на заповед за защита', 'чл.296, ал.1', 8),
    (9, 'Повторно неизпълнение на заповед за защита', 'чл.296, ал.4', 9);

drop table if exists analytics.dim_police_structure cascade;
create table if not exists analytics.dim_police_structure (
    police_structure_id smallint primary key,
    police_structure_name varchar(100) not null,
    police_structure_type varchar(30) not null,
    display_order smallint not null,

    constraint uq_police_structure_display_order unique (display_order),

    constraint chk_police_structure_type
        check (
            police_structure_type in (
                'national_directorate',
                'regional_directorate',
                'total'
            )
        ),

    constraint chk_police_structure_id_positive check (police_structure_id > 0),
    constraint chk_police_structure_display_order_positive check (display_order > 0));

insert into analytics.dim_police_structure (
    police_structure_id,
    police_structure_name,
    police_structure_type,
    display_order
)
values
    (1, 'ГДНП', 'national_directorate', 1),
    (2, 'ОБЩО', 'total', 2),
    (3, 'ОДМВР БЛАГОЕВГРАД', 'regional_directorate', 3),
    (4, 'ОДМВР БУРГАС', 'regional_directorate', 4),
    (5, 'ОДМВР ВАРНА', 'regional_directorate', 5),
    (6, 'ОДМВР ВЕЛИКО ТЪРНОВО', 'regional_directorate', 6),
    (7, 'ОДМВР ВИДИН', 'regional_directorate', 7),
    (8, 'ОДМВР ВРАЦА', 'regional_directorate', 8),
    (9, 'ОДМВР ГАБРОВО', 'regional_directorate', 9),
    (10, 'ОДМВР ДОБРИЧ', 'regional_directorate', 10),
    (11, 'ОДМВР КЪРДЖАЛИ', 'regional_directorate', 11),
    (12, 'ОДМВР КЮСТЕНДИЛ', 'regional_directorate', 12),
    (13, 'ОДМВР ЛОВЕЧ', 'regional_directorate', 13),
    (14, 'ОДМВР МОНТАНА', 'regional_directorate', 14),
    (15, 'ОДМВР ПАЗАРДЖИК', 'regional_directorate', 15),
    (16, 'ОДМВР ПЕРНИК', 'regional_directorate', 16),
    (17, 'ОДМВР ПЛЕВЕН', 'regional_directorate', 17),
    (18, 'ОДМВР ПЛОВДИВ', 'regional_directorate', 18),
    (19, 'ОДМВР РАЗГРАД', 'regional_directorate', 19),
    (20, 'ОДМВР РУСЕ', 'regional_directorate', 20),
    (21, 'ОДМВР СИЛИСТРА', 'regional_directorate', 21),
    (22, 'ОДМВР СЛИВЕН', 'regional_directorate', 22),
    (23, 'ОДМВР СМОЛЯН', 'regional_directorate', 23),
    (24, 'ОДМВР СОФИЯ', 'regional_directorate', 24),
    (25, 'ОДМВР СТАРА ЗАГОРА', 'regional_directorate', 25),
    (26, 'ОДМВР ТЪРГОВИЩЕ', 'regional_directorate', 26),
    (27, 'ОДМВР ХАСКОВО', 'regional_directorate', 27),
    (28, 'ОДМВР ШУМЕН', 'regional_directorate', 28),
    (29, 'ОДМВР ЯМБОЛ', 'regional_directorate', 29),
    (30, 'СДВР', 'regional_directorate', 30);

    
drop table if exists analytics.dim_offender_category cascade;
create table if not exists analytics.dim_offender_category (
    offender_category_id smallint primary key,
    offender_category_name varchar(100) not null,
    offender_category_type varchar(30) not null,
    display_order smallint not null,

    constraint uq_offender_category_name unique (offender_category_name),
    constraint uq_offender_category_display_order unique (display_order),
    constraint chk_offender_category_display_order_positive check (display_order > 0)
);


insert into analytics.dim_offender_category (
    offender_category_id,
    offender_category_name,
    offender_category_type,
    display_order
)
values
    (1, 'Общ брой', 'total', 1),
    (2, 'Жени', 'gender', 2),
    (3, 'Под 14 години', 'age', 3),
    (4, '14–17 години', 'age', 4),
    (5, '18–30 години', 'age', 5),
    (6, '31–40 години', 'age', 6),
    (7, 'Над 40 години', 'age', 7);


drop table if exists analytics.dim_location_category cascade;
create table analytics.dim_location_category (
    location_category_id smallint primary key,
    location_category_name varchar(100) not null,
    classification_type varchar(30) not null,
    display_order smallint not null,

    constraint uq_location_category_name unique (location_category_name),
    constraint uq_location_category_display_order unique (display_order),
    constraint chk_location_category_id_positive check (location_category_id > 0),
    constraint chk_location_classification_type
        check (
            classification_type in (
                'public_place',
                'geographic_area'
            )
        ),
    constraint chk_location_category_display_order_positive check (display_order > 0)
);


insert into analytics.dim_location_category (
    location_category_id,
    location_category_name,
    classification_type,
    display_order
)
values
    (1, 'Обществени места', 'public_place', 1),
    (2, 'Регионален център', 'geographic_area', 2),
    (3, 'Град', 'geographic_area', 3),
    (4, 'Село', 'geographic_area', 4),
    (5, 'Извън населено място', 'geographic_area', 5),
    (6, 'Вилна зона', 'geographic_area', 6),
    (7, 'Гранична зона', 'geographic_area', 7),
    (8, 'ГКПП', 'geographic_area', 8);


drop table if exists analytics.dim_crime_status cascade;
create table analytics.dim_crime_status (
    crime_status_id smallint primary key,
    crime_status_code varchar(20) not null,
    crime_status_name varchar(50) not null,
    display_order smallint not null,

    constraint uq_crime_status_code unique (crime_status_code),
    constraint uq_crime_status_name unique (crime_status_name),
    constraint uq_crime_status_display_order unique (display_order),
    constraint chk_crime_status_id_positive check (crime_status_id > 0),
    constraint chk_crime_status_display_order_positive check (display_order > 0)
);

insert into analytics.dim_crime_status (
    crime_status_id,
    crime_status_code,
    crime_status_name,
    display_order
)
values
    (1, 'registered', 'Регистрирани', 1),
    (2, 'solved', 'Разкрити', 2);


drop table if exists analytics.dim_date cascade;
create table analytics.dim_date (
    calendar_date date primary key,
    day_of_month smallint,
    day_of_week_number smallint,
    day_of_week_name varchar(20),
    month_number smallint,
    month_name varchar(20),
    quarter_number smallint,
    quarter_label varchar(20),
    calendar_year smallint,  
    is_weekend boolean
);

with cte_dates as (
    select 
        generated_date::date as calendar_date
    from 
        generate_series(
            date '2024-01-01',
            date '2027-12-31',
            interval '1 day'
        ) as dates(generated_date)
)
insert into analytics.dim_date (
    calendar_date,
    day_of_month,
    day_of_week_number,
    day_of_week_name,
    month_number,
    month_name,
    quarter_number,
    quarter_label,
    calendar_year,  
    is_weekend
)
select
	calendar_date,
	extract(day from calendar_date)::smallint,
	extract(ISODOW from calendar_date)::smallint,
    to_char(calendar_date, 'Day'),
	extract(month from calendar_date)::smallint,
    to_char(calendar_date, 'Month'),
	extract(quarter from calendar_date)::smallint,
	'Q' || extract(quarter from calendar_date),
	extract(year from calendar_date)::smallint,
	extract(isodow from calendar_date) in (6, 7)
from
	cte_dates;

