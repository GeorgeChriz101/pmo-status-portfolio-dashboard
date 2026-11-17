# Data Dictionary

## site_id

Original project site identifier.

## site_id_normalized

Standardized site identifier used for portfolio reporting.

Example:

SITE105 becomes SITE-105.

## milestone

Current network deployment activity.

Values include:

- Survey
- Permitting
- Equipment Delivery
- Installation
- Acceptance

## owner

Person responsible for the milestone.

## planned_date

Scheduled milestone date.

## percent_complete

Estimated completion percentage from 0 to 100.

## status

Current milestone status.

Values include:

- Not Started
- In Progress
- Complete

## dependency

Milestone that precedes the current activity.

## issue

Known problem affecting the project.

## issue_owner

Person responsible for resolving the issue.

## requested_decision

Stakeholder decision required to move the work forward.

## missing_owner

Flag identifying records without a milestone owner.

## missing_planned_date

Flag identifying records without a planned date.

## overdue

Flag identifying incomplete milestones whose planned date has passed.

## data_quality_issue

Combined indicator showing whether the record requires data-quality review.
