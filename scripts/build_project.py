import pandas as pd
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font
from pptx import Presentation

RAW = Path("data/raw")
PROCESSED = Path("data/processed")
REPORTS = Path("reports")
DOCS = Path("docs")

for folder in [RAW, PROCESSED, REPORTS, DOCS]:
    folder.mkdir(parents=True, exist_ok=True)

# -----------------------------------------
# 1. CREATE 60 SYNTHETIC SITE UPDATES
# -----------------------------------------

sites = [f"SITE-{i:03d}" for i in range(101, 121)]

milestones = [
    "Survey",
    "Permitting",
    "Equipment Delivery",
    "Installation",
    "Acceptance"
]

owners = [
    "Alex Johnson",
    "Priya Shah",
    "Michael Brown",
    "Sarah Lee",
    "Daniel Kim"
]

rows = []
base_date = pd.Timestamp("2027-05-01")

for i in range(60):
    site = sites[i % len(sites)]
    milestone = milestones[i % len(milestones)]
    planned_date = base_date + pd.Timedelta(days=i % 35)

    percent_complete = [0, 25, 50, 75, 100][i % 5]

    if percent_complete == 100:
        status = "Complete"
    elif percent_complete > 0:
        status = "In Progress"
    else:
        status = "Not Started"

    rows.append({
        "site_id": site,
        "milestone": milestone,
        "owner": owners[i % len(owners)],
        "planned_date": planned_date.strftime("%Y-%m-%d"),
        "percent_complete": percent_complete,
        "status": status,
        "dependency": (
            milestones[(i - 1) % 5]
            if i % 5 != 0
            else "None"
        ),
        "issue": (
            "Schedule delay"
            if i % 6 == 0
            else ""
        ),
        "issue_owner": (
            owners[(i + 1) % len(owners)]
            if i % 6 == 0
            else ""
        ),
        "requested_decision": (
            "Confirm recovery plan"
            if i % 6 == 0
            else ""
        )
    })

df = pd.DataFrame(rows)

# Seed inconsistent data
df.loc[3, "site_id"] = "site 104"
df.loc[9, "site_id"] = "SITE105"

# Missing owners
df.loc[14, "owner"] = ""
df.loc[31, "owner"] = ""

# Missing dates
df.loc[21, "planned_date"] = ""
df.loc[44, "planned_date"] = ""

df.to_csv(
    RAW / "site_updates_raw.csv",
    index=False
)

# -----------------------------------------
# 2. STANDARDIZATION
# -----------------------------------------

def normalize_site_id(value):
    value = str(value).upper().strip()
    value = value.replace(" ", "-")

    if value.startswith("SITE") and "-" not in value:
        value = value.replace("SITE", "SITE-", 1)

    return value

df["site_id_normalized"] = df[
    "site_id"
].apply(normalize_site_id)

# -----------------------------------------
# 3. DATA QUALITY
# -----------------------------------------

df["missing_owner"] = (
    df["owner"].isna()
    | (df["owner"].astype(str).str.strip() == "")
)

df["missing_planned_date"] = (
    df["planned_date"].isna()
    | (df["planned_date"].astype(str).str.strip() == "")
)

df["planned_date_parsed"] = pd.to_datetime(
    df["planned_date"],
    errors="coerce"
)

reporting_date = pd.Timestamp("2027-05-25")

df["overdue"] = (
    (df["planned_date_parsed"] < reporting_date)
    & (df["percent_complete"] < 100)
)

df["data_quality_issue"] = (
    df["missing_owner"]
    | df["missing_planned_date"]
)

df.to_csv(
    PROCESSED / "site_updates_cleaned.csv",
    index=False
)

# -----------------------------------------
# 4. PORTFOLIO SUMMARY
# -----------------------------------------

summary = pd.DataFrame({
    "Metric": [
        "Total Updates",
        "Unique Sites",
        "Average Completion %",
        "Completed Milestones",
        "Overdue Items",
        "Missing Owners",
        "Missing Planned Dates",
        "Open Issues"
    ],
    "Value": [
        len(df),
        df["site_id_normalized"].nunique(),
        round(df["percent_complete"].mean(), 1),
        int((df["status"] == "Complete").sum()),
        int(df["overdue"].sum()),
        int(df["missing_owner"].sum()),
        int(df["missing_planned_date"].sum()),
        int((df["issue"] != "").sum())
    ]
})

summary.to_csv(
    PROCESSED / "portfolio_summary.csv",
    index=False
)

# -----------------------------------------
# 5. PROGRESS DASHBOARD
# -----------------------------------------

progress = (
    df.groupby("site_id_normalized")
    .agg(
        average_completion=(
            "percent_complete",
            "mean"
        ),
        completed_milestones=(
            "status",
            lambda x: (x == "Complete").sum()
        ),
        total_updates=(
            "status",
            "count"
        )
    )
    .reset_index()
)

progress["average_completion"] = (
    progress["average_completion"].round(1)
)

progress.to_csv(
    PROCESSED / "dashboard_progress.csv",
    index=False
)

# -----------------------------------------
# 6. RISK DASHBOARD
# -----------------------------------------

risks = df[
    df["overdue"]
    | (df["issue"] != "")
    | df["data_quality_issue"]
][[
    "site_id_normalized",
    "milestone",
    "owner",
    "planned_date",
    "issue",
    "issue_owner",
    "overdue",
    "missing_owner",
    "missing_planned_date",
    "requested_decision"
]]

risks.to_csv(
    PROCESSED / "dashboard_risks.csv",
    index=False
)

# -----------------------------------------
# 7. UPCOMING WORK DASHBOARD
# -----------------------------------------

upcoming = df[
    (df["planned_date_parsed"] >= reporting_date)
    & (df["percent_complete"] < 100)
][[
    "site_id_normalized",
    "milestone",
    "owner",
    "planned_date",
    "dependency",
    "status"
]].sort_values("planned_date")

upcoming.to_csv(
    PROCESSED / "dashboard_upcoming_work.csv",
    index=False
)

# -----------------------------------------
# 8. EXCEPTION LOG
# -----------------------------------------

exceptions = df[
    df["data_quality_issue"]
][[
    "site_id",
    "site_id_normalized",
    "milestone",
    "owner",
    "planned_date",
    "missing_owner",
    "missing_planned_date"
]]

exceptions.to_csv(
    PROCESSED / "data_quality_exceptions.csv",
    index=False
)

# -----------------------------------------
# 9. RECONCILIATION
# -----------------------------------------

raw_count = len(
    pd.read_csv(RAW / "site_updates_raw.csv")
)

processed_count = len(df)

reconciliation = pd.DataFrame([{
    "raw_records": raw_count,
    "processed_records": processed_count,
    "difference": raw_count - processed_count,
    "reconciled": raw_count == processed_count
}])

reconciliation.to_csv(
    PROCESSED / "reconciliation_check.csv",
    index=False
)

# -----------------------------------------
# 10. EXCEL REPORT
# -----------------------------------------

excel_file = (
    REPORTS / "pmo_portfolio_status_dashboard.xlsx"
)

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    df.to_excel(
        writer,
        sheet_name="Cleaned Updates",
        index=False
    )

    summary.to_excel(
        writer,
        sheet_name="Portfolio Summary",
        index=False
    )

    progress.to_excel(
        writer,
        sheet_name="Progress Dashboard",
        index=False
    )

    risks.to_excel(
        writer,
        sheet_name="Risk Dashboard",
        index=False
    )

    upcoming.to_excel(
        writer,
        sheet_name="Upcoming Work",
        index=False
    )

    exceptions.to_excel(
        writer,
        sheet_name="Data Quality Issues",
        index=False
    )

    reconciliation.to_excel(
        writer,
        sheet_name="Reconciliation",
        index=False
    )

wb = load_workbook(excel_file)

for ws in wb.worksheets:
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions

    for cell in ws[1]:
        cell.font = Font(bold=True)

    for column in ws.columns:
        max_length = 0
        letter = column[0].column_letter

        for cell in column:
            try:
                max_length = max(
                    max_length,
                    len(str(cell.value or ""))
                )
            except Exception:
                pass

        ws.column_dimensions[letter].width = min(
            max_length + 2,
            45
        )

wb.save(excel_file)

# -----------------------------------------
# 11. WEEKLY STATUS POWERPOINT
# -----------------------------------------

prs = Presentation()

slide = prs.slides.add_slide(
    prs.slide_layouts[0]
)

slide.shapes.title.text = (
    "Weekly PMO Portfolio Status"
)

slide.placeholders[1].text = (
    "Network Services Site Deployment Portfolio"
)

slide = prs.slides.add_slide(
    prs.slide_layouts[1]
)

slide.shapes.title.text = "Portfolio Summary"

slide.placeholders[1].text = (
    f"Total updates: {len(df)}\n"
    f"Unique sites: {df['site_id_normalized'].nunique()}\n"
    f"Average completion: {df['percent_complete'].mean():.1f}%\n"
    f"Overdue items: {df['overdue'].sum()}\n"
    f"Open issues: {(df['issue'] != '').sum()}"
)

slide = prs.slides.add_slide(
    prs.slide_layouts[1]
)

slide.shapes.title.text = "Key Risks and Issues"

risk_lines = []

for _, row in risks.head(8).iterrows():
    issue = row["issue"]

    if not issue:
        issue = "Data quality or schedule issue"

    risk_lines.append(
        f"{row['site_id_normalized']} - "
        f"{row['milestone']} - {issue}"
    )

slide.placeholders[1].text = "\n".join(
    risk_lines
)

slide = prs.slides.add_slide(
    prs.slide_layouts[1]
)

slide.shapes.title.text = "Upcoming Work"

upcoming_lines = []

for _, row in upcoming.head(8).iterrows():
    upcoming_lines.append(
        f"{row['site_id_normalized']} - "
        f"{row['milestone']} - "
        f"{row['planned_date']}"
    )

slide.placeholders[1].text = "\n".join(
    upcoming_lines
)

slide = prs.slides.add_slide(
    prs.slide_layouts[1]
)

slide.shapes.title.text = "Requested Decisions"

decision_rows = df[
    df["requested_decision"] != ""
]

decision_lines = []

for _, row in decision_rows.head(8).iterrows():
    decision_lines.append(
        f"{row['site_id_normalized']}: "
        f"{row['requested_decision']} "
        f"(Owner: {row['issue_owner']})"
    )

slide.placeholders[1].text = "\n".join(
    decision_lines
)

ppt_file = REPORTS / "weekly_pmo_status_deck.pptx"

prs.save(ppt_file)

print("")
print("================================")
print("PROJECT BUILD COMPLETE")
print("================================")
print("Raw updates:", len(df))
print(
    "Unique sites:",
    df["site_id_normalized"].nunique()
)
print("Dashboard views: 3")
print("Excel:", excel_file)
print("PowerPoint:", ppt_file)
