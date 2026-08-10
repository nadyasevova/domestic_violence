SELECT 'CREATE DATABASE domestic_violence'
WHERE NOT EXISTS (
    SELECT 1
    FROM pg_database
    WHERE datname = 'domestic_violence'
)
\gexec