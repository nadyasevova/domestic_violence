create schema if not exists analytics;


drop table if exists analytics.dim_crime_type cascade;
create table if not exists analytics.dim_crime_type (
    crime_type_id smallint generated always as identity primary key,
    crime_type_name varchar(100) not null,
    criminal_code_article varchar(100) not null,
    display_order smallint not null,

    constraint uq_crime_type_name unique (crime_type_name),
    constraint uq_criminal_code_article unique (criminal_code_article),
    constraint uq_crime_type_display_order unique (display_order),
    constraint chk_crime_type_display_order_positive check (display_order > 0)
);

insert into analytics.dim_crime_type 
    (crime_type_name, criminal_code_article, display_order)
values
    ('Убийство', 'чл.116, ал.1, т.6а', 1),
    ('Телесна повреда', 'чл.131, ал.1, т.5а', 2),
    ('Отвличане', 'чл.142, ал.2, т.5а', 3),
    ('Лишаване от свобода', 'чл.142а, ал.4', 4),
    ('Принуда', 'чл.143, ал.3, т.1', 5),
    ('Закана', 'чл.144, ал.3, т.3', 6),
    ('Следене', 'чл.144а, ал.3', 7),
    ('Неизпълнение на заповед за защита', 'чл.296, ал.1', 8),
    ('Повторно неизпълнение на заповед за защита', 'чл.296, ал.4', 9)
on conflict (criminal_code_article) do update
set
    crime_type_name = excluded.crime_type_name,
    display_order = excluded.display_order;