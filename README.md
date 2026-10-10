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
- validates totals, categories, and reporting periods;
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
- registered crimes by location type;
- established offenders by age group and gender.

Source: [Bulgarian Ministry of Interior](https://www.mvr.bg/gdnp/%D0%B4%D0%B5%D0%B9%D0%BD%D0%BE%D1%81%D1%82%D0%B8/%D0%B4%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%BE-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5/%D1%81%D1%82%D0%B0%D1%82%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0/%D1%80%D0%B5%D0%B3%D0%B8%D1%81%D1%82%D1%80%D0%B8%D1%80%D0%B0%D0%BD%D0%B8-%D0%BF%D1%80%D0%B5%D1%81%D1%82%D1%8A%D0%BF%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BE%D0%BC%D0%B0%D1%88%D0%BD%D0%BE-%D0%BD%D0%B0%D1%81%D0%B8%D0%BB%D0%B8%D0%B5)

No personal or case-level information is used in this project.

## Data pipeline

```mermaid
flowchart LR
    A["Official XLS reports"] --> B["Python extraction"]
    B --> C["PostgreSQL staging"]
    C --> D["Validation checks"]
    D --> E["Analytical model"]
    E --> F["Power BI report"]
```

The source files are preserved in their original form. Data cleaning and transformation are performed separately so that published values can always be traced back to their source.

## Data model

The analytical model separates measurable events from descriptive dimensions.

The main dimensions include:

- police region;
- crime type;
- location type;
- offender category;
- reporting period.

Key dimensions use predefined IDs that remain consistent when new reporting periods are added or source files are updated.

## Data validation

The loading and transformation process includes checks for:

- duplicate source cells;
- missing or unexpected values;
- inconsistent crime classifications;
- invalid reporting periods;
- published totals versus calculated totals;
- consistency between regional and national values;
- changes in source-file structure.

Detected discrepancies are documented rather than silently corrected.

This distinction is important because the objective is to analyze the published data while preserving its original meaning and limitations.

## Regional analysis

The first completed Power BI page focuses on regional patterns and changes over time.

Users can:

- switch between reporting years;
- select a region from the map or ranking chart;
- compare regional totals;
- examine the distribution by crime type;
- compare monthly trends for up to four selected regions;
- view exact values through report tooltips.

The map uses a consistent color scale across reporting years so that differences between years remain visually comparable.

## Initial findings

For 2024:

- bodily injury was the most frequently registered crime type, accounting for 70.8% of the reported total;
- non-compliance with a protection order was the second-largest category;
- Burgas and Sofia-city recorded the highest regional totals;
- a small number of crime types accounted for most registered crimes;
- substantial differences were visible between police regions.

These findings describe police-registered crimes and should not be interpreted as estimates of the actual prevalence of domestic violence.

## Limitations

- The data represents crimes registered by the police, not all incidents of domestic violence.
- Differences between regions may reflect population size, reporting behaviour, police practices, or access to institutions.
- Regional values are not currently normalized by population.
- Data for 2026 covers only part of the year and should not be compared directly with complete annual totals.
- The source reports provide aggregated statistics and do not support case-level analysis.
- The analysis identifies patterns and associations but does not establish causal relationships.

## Technologies

- **Python and pandas** — extraction, cleaning, and transformation
- **PostgreSQL** — staging, validation, and analytical storage
- **SQL** — data quality checks and analytical queries
- **Power BI and DAX** — data modelling, interaction design, and visualization
- **Git and GitHub** — version control and project documentation
- **uv** — Python environment and dependency management
- **pytest and Ruff** — testing and code quality

## Repository structure

```text
.
├── config/          # Project configuration
├── data/
│   └── raw/         # Original source files by reporting year
├── docs/            # Documentation and report images
├── logs/            # Processing logs
├── notebooks/       # Exploratory analysis
├── output/          # Generated outputs
├── powerbi/         # Power BI report file
├── sql/             # Schema, validation, and analytical SQL
├── src/             # Python extraction and loading code
└── tests/           # Automated tests
```

## View the Power BI report

The current Power BI report can be downloaded here:

[Download the Power BI report](powerbi/Domestic_Violence_Regional_Analysis_v1_0.pbix)

Power BI Desktop is required to open the `.pbix` file.

The report contains imported public data, so it can be explored without connecting to the original PostgreSQL database. Refreshing the data requires access to the project database and source files.

## Project status

### Completed

- source-file organization by reporting year;
- extraction and loading of the three source datasets;
- PostgreSQL staging tables;
- analytical dimensions and fact tables;
- data validation queries;
- regional analysis Power BI page;
- dynamic report context and interactive filtering.

### In progress

- crime location analysis;
- offender age and gender analysis;
- expanded automated tests;
- final documentation;
- additional analytical insights.

## Planned report pages

1. **Regional Analysis** — completed
2. **Crime Location Analysis** — in development
3. **Offender Characteristics** — in development

## Author

**Nadya Sevova**