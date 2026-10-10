# Domestic Violence in Bulgaria — Data Analytics Project

An end-to-end data analytics project examining registered domestic violence crimes in Bulgaria by region, crime type, location, and offender characteristics.

The project transforms publicly available XLS reports into a structured and validated analytical model using Python, PostgreSQL, SQL, and Power BI.

> **Current status:** The Regional Analysis report page is complete. Two additional pages covering crime locations and offender characteristics are in development.

## Report preview

![Regional analysis dashboard](docs/images/regional_analysis_dashboard.png)

The completed Power BI page provides:

- year-based analysis for 2024, 2025, and 2026;
- geographic distribution of registered crimes;
- ranking of the regions with the highest registered crime counts;
- breakdown by crime type;
- monthly trend comparison between selected regions;
- dynamic titles and insights based on the current filter context.

The monthly trend section covers the complete available period and is intentionally independent of the year filter applied to the upper section.

## Project objective

The source data is published as separate XLS reports that are not immediately suitable for analysis.

The objective of this project is to build a reproducible analytical workflow that:

- extracts and standardizes the source files;
- preserves the original published values;
- loads the data into PostgreSQL staging tables;
- performs SQL-based data quality checks on totals, categories, and reporting periods;
- transforms the data into an analytical model;
- presents the results through clear and responsible data visualizations.

The project is designed both as an analysis of the available data and as a demonstration of an end-to-end analytics workflow.

## Data

The project uses publicly available statistical reports published by the Bulgarian Ministry of Interior.

The current dataset covers:

- 2024 — complete year;
- 2025 — complete year;
- 2026 — January through June.

The source reports contain information about:

- registered crimes by police region;
- registered crimes by settlement and location type;
- established offenders by age group and gender.

Source: [Bulgarian Ministry of Interior](https://www.mvr.bg/gdnp/%D0%B4%D0%B5%D0%B9%D0%BD%D0%BE%D1%81%D1%82%D0%B8/%D0%B4%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%BE-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5/%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B8%D1%80%D0%B0%D0%BD%D0%B8-%D0%BF%D1%80%D0%B5%D1%81%D1%82%D1%8A%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%BE-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5)

No personal or case-level information is used in this project.

## Data pipeline

```mermaid
flowchart LR
    A["Official XLS reports"] --> B["Python extraction"]
    B --> C["PostgreSQL staging"]
    C --> D["SQL validation (manual)"]
    D --> E["Analytical model"]
    E --> F["Power BI report"]
```

The original XLS files are preserved without modification. Data cleaning and transformation are performed separately from the raw data to support traceability and reproducibility.


## Data model

The analytical model separates aggregated statistical measures from descriptive dimensions.

The main dimensions include:

- police region;
- crime type;
- location type;
- offender category;
- reporting period.

Key dimensions use predefined IDs that remain consistent when new reporting periods are added or source files are updated.

## Data validation

## Data validation

Data quality checks are currently performed manually using SQL queries to identify potential inconsistencies in the source data.

Identified discrepancies are documented, while the original published values are preserved without modification.

Automated tests have not yet been implemented.

## Regional analysis

The first completed Power BI page focuses on regional patterns and changes over time.

Users can:

- switch between reporting years;
- select a region from the map or ranking chart;
- compare the number of registered crimes across regions;
- examine the distribution by crime type;
- compare monthly trends for up to four selected regions;
- view exact values through report tooltips.

The map uses a consistent color scale across reporting years so that differences between years remain visually comparable.

The monthly trend chart displays the full available reporting period, independently of the year selection applied to the upper section of the report.

## Initial findings

For 2024:

- bodily injury was the most frequently registered crime type, accounting for 70.8% of the reported total;
- non-compliance with a protection order was the second-largest category;
- Burgas and Sofia-city recorded the highest regional totals;

These findings describe police-registered crimes and should not be interpreted as estimates of the actual prevalence of domestic violence.

## Limitations

- The data represents crimes registered by the police, not all incidents of domestic violence.
- Differences between regions may reflect population size, reporting behaviour, police practices, or access to institutions.
- Regional values are not currently normalized by population.
- Data for 2026 covers only part of the year and should not be compared directly with complete annual totals.
- The source reports provide aggregated statistics and do not support case-level analysis.
- The analysis is descriptive and does not establish causal relationships.

## Technologies

- Python and pandas — extraction, cleaning, and transformation
- PostgreSQL — staging and analytical storage
- SQL — data quality checks and analytical queries
- Power BI and DAX — data modelling, interaction design, and visualization
- Git and GitHub — version control and project documentation
- uv — Python environment and dependency management

## Repository structure

```text
.
├── config/          # Project configuration
├── data/
│   └── raw/         # Original source files by reporting year
├── docs/            # Documentation and report images
├── powerbi/         # Power BI report file
├── sql/             # Schema, validation, and analytical SQL
├── src/             # Python extraction and loading code


## Reproducing the analysis

Step-by-step instructions for setting up the environment, loading the source data, building the analytical model, and refreshing the Power BI report will be added as the documentation is completed.```

## View the Power BI report

The current Power BI report can be downloaded here:

[Download the Power BI report](powerbi/Domestic_Violence_Regional_Analysis_v1_0.pbix)

Power BI Desktop is required to open the `.pbix` file.

The report contains imported public data, so it can be explored without connecting to the original PostgreSQL database. Refreshing the data requires access to the PostgreSQL database used by the project.

## Project status

### Completed

- source-file organization by reporting year;
- extraction and loading of the three source datasets;
- PostgreSQL staging tables;
- analytical dimensions and fact tables;
- SQL data validation queries;
- regional analysis Power BI page;
- dynamic report context and interactive filtering.

### In progress

- crime location analysis;
- offender age and gender analysis;
- final documentation;
- additional analytical insights.

## Planned report pages

1. **Regional Analysis** — completed
2. **Crime Location Analysis** — in development
3. **Offender Characteristics** — in development

## Author

**Nadya Sevova**