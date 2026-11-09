# Pharmacovigilance Data Quality & Risk Review Analytics

## Project overview

An exploratory pharmacovigilance analytics project using publicly available FDA adverse-event reporting data. The project demonstrates data extraction, data quality validation, rules-based review prioritisation, exploratory reaction categorisation and interactive dashboard reporting.

## Objectives

- Extract and prepare adverse-event reports using the openFDA API.
- Assess selected data quality indicators.
- Apply transparent rules to flag reports for potential human review.
- Explore reaction terms using illustrative analytical categories.
- Present findings through an interactive Streamlit dashboard.

## Analytical workflow

1. Data extraction and preparation.
2. Data quality assessment.
3. Rules-based review prioritisation.
4. Exploratory reaction categorisation.
5. Interactive dashboard development.

## Key results

| Measure | Result |
|---|---:|
| Reports analysed | 900 |
| Reaction records | 2,460 |
| Unique reaction terms | 855 |
| Reports flagged for potential review | 130 |
| Reports with missing key data | 0 |
| Reports with invalid seriousness codes | 0 |

The review rules flagged approximately 14.4% of reports in the sample.

## Dashboard

- Overview and report seriousness.
- Data quality indicators.
- Review prioritisation and flag reasons.
- Reaction category distribution and most frequent terms.
- Interactive report explorer.
- Interpretation and limitations.

## Technology

Python, pandas, requests, Streamlit, openFDA API, Google Colab and GitHub.

## Repository structure

- `app.py` – Streamlit dashboard.
- `pv_analysis.py` – reusable analysis functions.
- `pv_reports_review.csv` – prepared report-level dataset.
- `pv_reactions_categorised.csv` – reaction-level dataset.
- `requirements.txt` – application dependencies.
- `notebooks/` – analytical notebooks.

## Running the application

Install dependencies:

    pip install -r requirements.txt

Run the dashboard:

    streamlit run app.py

Keep both CSV datasets in the repository root alongside `app.py`.

## Data source

FDA Adverse Event Reporting System (FAERS), accessed through the [openFDA API](https://open.fda.gov/apis/drug/event/).

## Limitations

- Spontaneous reports do not establish causality.
- Report counts cannot estimate adverse-event incidence or probability.
- Review flags use illustrative rules and are not validated pharmacovigilance triage criteria.
- Reaction categories are limited analytical groupings, not comprehensive or validated MedDRA coding.
- Missing information does not mean an event did not occur.
- The 900-report sample should not be interpreted as representative of all FAERS reporting activity.

**Intended use:** An exploratory analytics and review-support prototype for educational and portfolio demonstration. It is not a validated pharmacovigilance system and does not replace qualified safety assessment or expert review.
