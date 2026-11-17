# Validation Rules

The project validates site updates before portfolio reporting.

## Rule 1 - Site ID Standardization

Site identifiers are converted into a consistent format.

Examples:

site 104 becomes SITE-104.

SITE105 becomes SITE-105.

## Rule 2 - Missing Owner

A record is flagged when no milestone owner is assigned.

## Rule 3 - Missing Planned Date

A record is flagged when the planned milestone date is unavailable.

## Rule 4 - Overdue Milestone

A milestone is considered overdue when:

- The planned date is before the reporting date.
- Percent complete is below 100.

## Rule 5 - Row Count Reconciliation

Raw and processed record counts are compared.

Expected result:

60 raw records.

60 processed records.

Difference of zero.

These rules help prevent incomplete or inconsistent data from creating inaccurate PMO reports.
