# Data Quality Notes

## Crimes by region

### Published total differs from the regional sum

One discrepancy was found in the January 2024 data:

- Source file: `data/raw/2024/crimes_by_region.xls`
- Source sheet: `януари 2024 г.`
- Criminal Code article: `чл.144, ал.3, т.3`
- Published total: 17
- Calculated regional total: 16
- Difference: 1

The source values are preserved without correction in the staging table.

The `ОБЩО` row represents the published total, while the remaining rows
contain the values reported by the individual police directorates.
The discrepancy must be considered when national totals are calculated
in the analytics layer.