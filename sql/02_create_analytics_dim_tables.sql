create schema if not exists analytics;


drop table if exists analytics.dim_crime_type;
create table if not exists analytics.dim_crime_type (
    crime_type_id smallint primary key,
    crime_type_name varchar(100) not null,
    criminal_code_article varchar(100),
    crime_type_level varchar(20) not null,
    display_order smallint not null,

    constraint uq_crime_type_name unique (crime_type_name),
    constraint uq_criminal_code_article unique (criminal_code_article),
    constraint uq_crime_type_display_order unique (display_order),
    constraint chk_crime_type_display_order_positive check (display_order > 0),

    constraint chk_crime_type_level
        check (
            crime_type_level in (
                'total',
                'detail'
            )
        ),
    constraint chk_criminal_code_article_by_level
    check (
        (crime_type_level = 'total' and criminal_code_article is null)
        or
        (crime_type_level = 'detail' and criminal_code_article is not null)
    )        

);

insert into analytics.dim_crime_type 
    (crime_type_id, crime_type_name, criminal_code_article, crime_type_level, display_order)
values
    (1, 'Общо престъпления', null, 'total', 1),
    (2, 'Убийство', 'чл.116, ал.1, т.6а', 'detail', 2),
    (3, 'Телесна повреда', 'чл.131, ал.1, т.5а', 'detail',3),
    (4, 'Отвличане', 'чл.142, ал.2, т.5а', 'detail',4),
    (5, 'Лишаване от свобода', 'чл.142а, ал.4', 'detail',5),
    (6, 'Принуда', 'чл.143, ал.3, т.1', 'detail',6),
    (7, 'Закана', 'чл.144, ал.3, т.3', 'detail',7),
    (8, 'Следене', 'чл.144а, ал.3', 'detail',8),
    (9, 'Неизпълнение на заповед за защита', 'чл.296, ал.1', 'detail', 9),
    (10, 'Повторно неизпълнение на заповед за защита', 'чл.296, ал.4', 'detail', 10);


drop table if exists analytics.dim_district;
create table analytics.dim_district (
    district_id smallint primary key,
    district_name varchar(50) not null unique,
    map_district_code varchar(3) not null unique,

    constraint chk_district_id_positive
        check (district_id > 0)
);


insert into analytics.dim_district (
    district_id,
    district_name,
    map_district_code
)
values
    (1, 'Благоевград', 'BLG'),
    (2, 'Бургас', 'BGS'),
    (3, 'Варна', 'VAR'),
    (4, 'Велико Търново', 'VTR'),
    (5, 'Видин', 'VID'),
    (6, 'Враца', 'VRC'),
    (7, 'Габрово', 'GAB'),
    (8, 'Добрич', 'DOB'),
    (9, 'Кърджали', 'KRZ'),
    (10, 'Кюстендил', 'KNL'),
    (11, 'Ловеч', 'LOV'),
    (12, 'Монтана', 'MON'),
    (13, 'Пазарджик', 'PAZ'),
    (14, 'Перник', 'PER'),
    (15, 'Плевен', 'PVN'),
    (16, 'Пловдив', 'PDV'),
    (17, 'Разград', 'RAZ'),
    (18, 'Русе', 'RSE'),
    (19, 'Силистра', 'SLS'),
    (20, 'Сливен', 'SLV'),
    (21, 'Смолян', 'SML'),
    (22, 'София-област', 'SFO'),
    (23, 'Стара Загора', 'SZR'),
    (24, 'Търговище', 'TGV'),
    (25, 'Хасково', 'HKV'),
    (26, 'Шумен', 'SHU'),
    (27, 'Ямбол', 'JAM'),
    (28, 'София-град', 'SOF');

drop table if exists analytics.dim_police_structure;
create table if not exists analytics.dim_police_structure (
    police_structure_id smallint primary key,
    police_structure_name varchar(100) not null,
    police_structure_type varchar(30) not null,
    district_id smallint,
    display_order smallint not null,

    foreign key (district_id) references analytics.dim_district (district_id),
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
    district_id,
    display_order
)
values
    (1, 'ГДНП', 'national_directorate', null, 1),
    (2, 'ОБЩО', 'total', null, 2),
    (3, 'ОДМВР БЛАГОЕВГРАД', 'regional_directorate', 1, 3),
    (4, 'ОДМВР БУРГАС', 'regional_directorate', 2, 4),
    (5, 'ОДМВР ВАРНА', 'regional_directorate', 3, 5),
    (6, 'ОДМВR ВЕЛИКО ТЪРНОВО', 'regional_directorate', 4, 6),
    (7, 'ОДМВР ВИDИН', 'regional_directorate', 5, 7),
    (8, 'ОДMВR ВРАЦА', 'regional_directorate', 6, 8),
    (9, 'ОДMВR ГAБРОВO', 'regional_directorate', 7, 9),
    (10, 'ОДМВР ДОБРИЧ', 'regional_directorate', 8, 10),
    (11, 'ОДМВР КЪРДЖАЛИ', 'regional_directorate', 9, 11),
    (12, 'ОДМВР КЮСТЕНДИЛ', 'regional_directorate', 10, 12),
    (13, 'ОДМВR ЛOВEЧ', 'regional_directorate', 11, 13),
    (14, 'ОДМВR МОНТАНА', 'regional_directorate', 12, 14),
    (15, 'ОДМВR ПАЗАРДЖИК', 'regional_directorate', 13, 15),
    (16, 'ОДМВR ПЕРНИК', 'regional_directorate', 14, 16),
    (17, 'ОДМВR ПЛЕВЕН', 'regional_directorate', 15, 17),
    (18, 'ОДМВР ПЛОВДИВ', 'regional_directorate', 16, 18),
    (19, 'ОДМВР РАЗГРАД', 'regional_directorate', 17, 19),
    (20, 'ОДМВR РУСЕ', 'regional_directorate', 18, 20),
    (21, 'ОДМВR СИЛИСТРА', 'regional_directorate', 19, 21),
    (22, 'ОДМВР СЛИВЕН', 'regional_directorate', 20, 22),
    (23, 'ОДМВР СМОЛЯН', 'regional_directorate', 21, 23),
    (24, 'ОДМВР СОФИЯ', 'regional_directorate', 22, 24),
    (25, 'ОДМВR СТАРА ЗАГОРА', 'regional_directorate', 23, 25),
    (26, 'ОДМВR ТЪРГОВИЩЕ', 'regional_directorate', 24, 26),
    (27, 'ОДМВR ХАСКОВО', 'regional_directorate', 25, 27),
    (28, 'ОДМВР ШУМЕН', 'regional_directorate', 26, 28),
    (29, 'ОДМВR ЯMБOЛ', 'regional_directorate', 27, 29),
    (30, 'СДВR', 'regional_directorate',28, 30);

    
drop table if exists analytics.dim_offender_category;
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


drop table if exists analytics.dim_location_category;
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


drop table if exists analytics.dim_crime_status;
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


drop table if exists analytics.dim_date;
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



drop table if exists analytics.crime_type_mapping;
create table analytics.crime_type_mapping (
    source_crime_type_raw varchar(100) primary key,
    crime_type_id smallint not null,

    foreign key (crime_type_id) references analytics.dim_crime_type (crime_type_id)
);

insert into analytics.crime_type_mapping (
    source_crime_type_raw,
    crime_type_id
)
values
    ('Престъпления в усл. на дом. насилие', 1),
    ('- убийство', 2),
    ('- тел. повреда', 3),
    ('- отвличане', 4),
    ('- лишаване от свобода', 5),
    ('- принуда', 6),
    ('- закана', 7),
    ('- следене', 8),
    ('- неизп. защита', 9),
    ('- повт. неизп. защита', 10);