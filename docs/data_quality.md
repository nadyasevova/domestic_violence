# Data Quality Notes

## Crimes by region

### Published total differs from the regional sum

One discrepancy was identified in the January 2024 data:

- Source file: `data/raw/2024/crimes_by_region.xls`
- Source sheet: `януари 2024 г.`
- Criminal Code article: `чл. 144, ал. 3, т. 3`
- Published total: `17`
- Calculated regional total: `16`
- Difference: `1`

The source values are preserved without correction in the staging table.

The `ОБЩО` row contains the published national total, while the remaining rows contain the values reported by the individual police directorates. This discrepancy must therefore be considered when national totals are calculated in the analytics layer.

## Established offenders

### Validation by age group

For each reporting month and crime type, the published total number of established offenders must equal the sum of all age groups:

- under 14 years;
- 14–17 years;
- 18–30 years;
- 31–40 years;
- over 40 years.

Validation rule:

```text
total offenders =
    offenders under 14
    + offenders aged 14–17
    + offenders aged 18–30
    + offenders aged 31–40
    + offenders over 40
```

A difference indicates a possible extraction, transformation, or source-data quality issue.

### Derived number of male offenders

The source publishes the total number of established offenders and the number of female offenders, but it does not provide a separate value for male offenders.

The number of male offenders may be derived as:

```text
male offenders = total offenders - female offenders
```

This calculation assumes that:

- the total includes all established offenders;
- the female category includes all established female offenders;
- the source contains no additional or unspecified sex category.

Until these assumptions are confirmed by the source methodology, the number of male offenders must be presented as a derived value rather than a directly published measure.