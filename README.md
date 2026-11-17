# PMO Status Reporting and Portfolio Dashboard

A PMO portfolio project demonstrating how network deployment updates can be consolidated, validated, analyzed, and converted into management reporting.

## Project Overview

This project processes 60 synthetic network site updates.

The workflow standardizes project records, performs data-quality checks, calculates portfolio metrics, identifies risks, tracks upcoming work, reconciles totals, and prepares stakeholder reporting.

## Tools Used

- Python
- pandas
- Excel
- openpyxl
- Power BI-ready CSV datasets
- PowerPoint
- Git

## Key Features

- 60 synthetic site updates
- Site ID standardization
- Missing owner validation
- Missing planned date validation
- Overdue milestone detection
- Portfolio completion metrics
- Open issue tracking
- Three dashboard views
- Data-quality exception log
- Row-count reconciliation
- Excel portfolio workbook
- Power BI-ready datasets
- Weekly PMO PowerPoint deck
- Supporting project documentation

## Project Structure

pmo-status-portfolio-dashboard/

data/raw/
- site_updates_raw.csv

data/processed/
- site_updates_cleaned.csv
- portfolio_summary.csv
- dashboard_progress.csv
- dashboard_risks.csv
- dashboard_upcoming_work.csv
- data_quality_exceptions.csv
- reconciliation_check.csv

reports/
- pmo_portfolio_status_dashboard.xlsx
- weekly_pmo_status_deck.pptx

docs/
- data_dictionary.md
- validation_rules.md
- project_methodology.md
- dashboard_guide.md
- status_reporting_process.md
- status_meeting_template.md
- reconciliation_guide.md
- project_summary.md

scripts/
- build_project.py

README.md
requirements.txt
.gitignore

## Reporting Workflow

Site Updates

↓

Standardization

↓

Data Validation

↓

Portfolio Metrics

↓

Progress / Risk / Upcoming Work Views

↓

Reconciliation

↓

Excel and Power BI-ready Reporting

↓

Weekly PowerPoint Status Update

## Dashboard Views

### Progress

Shows completion and milestone progress by site.

### Risks

Shows overdue work, project issues, missing information, ownership, and requested decisions.

### Upcoming Work

Shows planned milestones, dates, owners, and dependencies.

## Excel Workbook

The workbook contains:

- Cleaned Updates
- Portfolio Summary
- Progress Dashboard
- Risk Dashboard
- Upcoming Work
- Data Quality Issues
- Reconciliation

## Power BI

The processed dashboard CSV files can be imported into Power BI for visualization.

## Weekly Status Deck

The PowerPoint summarizes:

- Portfolio progress
- Risks and issues
- Upcoming work
- Requested decisions

## Run the Project

Activate the virtual environment:

    source .venv/bin/activate

Run:

    python scripts/build_project.py

## Purpose

This project demonstrates practical PMO skills in portfolio reporting, schedule monitoring, data validation, risk reporting, reconciliation, stakeholder communication, and management reporting.

All project data is synthetic and created for portfolio demonstration purposes.
