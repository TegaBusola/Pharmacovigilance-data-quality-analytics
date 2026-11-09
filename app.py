
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# Page configuration
st.set_page_config(
    page_title="Pharmacovigilance Analytics",
    page_icon="📊",
    layout="wide"
)


# Dashboard styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1F33;
        color: #F2F5F8;
    }

    [data-testid="stHeader"] {
        background-color: #0B1F33;
    }

    [data-testid="stMetric"] {
        background-color: #142E46;
        border: 1px solid #29465F;
        padding: 18px 20px;
        border-radius: 10px;
    }

    [data-testid="stMetricLabel"] {
        color: #C4D3E0;
    }

    [data-testid="stMetricValue"] {
        color: #FFFFFF;
    }

    h1, h2, h3 {
        color: #FFFFFF;
    }

    p, li, label {
        color: #E0E8EF;
    }

    [data-testid="stCaptionContainer"] {
        color: #B4C5D4;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #29465F;
        border-radius: 8px;
    }

    hr {
        border-color: #29465F;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Project data locations
PROJECT_FOLDER = Path(__file__).resolve().parent

REPORTS_PATH = PROJECT_FOLDER / "pv_reports_review.csv"
REACTIONS_PATH = PROJECT_FOLDER / "pv_reactions_categorised.csv"


# Load dashboard datasets
@st.cache_data
def load_data():

    reports = pd.read_csv(REPORTS_PATH)
    reactions = pd.read_csv(REACTIONS_PATH)

    return reports, reactions


reports, reactions = load_data()


# Dashboard title
st.title("Pharmacovigilance Analytics")

st.caption(
    "Adverse-event data quality, review prioritisation "
    "and reaction analysis"
)

st.divider()


# Headline metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Reports analysed", f"{len(reports):,}")

with col2:
    flagged = reports["review_required"].sum()
    st.metric("Reports flagged for review", f"{flagged:,}")

with col3:
    st.metric("Reaction records", f"{len(reactions):,}")

with col4:
    unique_terms = reactions["reaction_term"].nunique()
    st.metric("Unique reaction terms", f"{unique_terms:,}")


# Overview section
st.header("Overview")

st.markdown(
    """
    This dashboard provides an exploratory view of publicly
    available adverse-event reports, including report seriousness,
    data quality, review prioritisation and reaction patterns.
    """
)


# Report seriousness distribution
st.subheader("Report seriousness")

seriousness_counts = (
    reports["serious"]
    .map({
        1: "Serious",
        2: "Not classified as serious"
    })
    .fillna("Unknown")
    .value_counts()
)

# Donut chart
seriousness_colours = {
    "Serious": "#56B4E9",
    "Not classified as serious": "#E69F00",
    "Unknown": "#B8A1CF"
}

fig = px.pie(
    names=seriousness_counts.index,
    values=seriousness_counts.values,
    hole=0.58,
    color=seriousness_counts.index,
    color_discrete_map=seriousness_colours
)

fig.update_traces(
    textposition="inside",
    textinfo="label+percent",
    textfont=dict(
        color="#FFFFFF",
        size=13
    ),
    hovertemplate=(
        "<b>%{label}</b><br>"
        "Reports: %{value:,}<br>"
        "Percentage: %{percent}"
        "<extra></extra>"
    )
)

fig.update_layout(
    showlegend=False,
    height=350,
    margin=dict(l=10, r=10, t=15, b=15),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="#F2F5F8",
        size=13
    )
)

chart_col, breakdown_col = st.columns([2, 1])

with chart_col:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

with breakdown_col:
    st.write("**Report breakdown**")

    for category, count in seriousness_counts.items():
        percentage = count / len(reports) * 100

        st.write(
            f"**{category}:** {count:,} ({percentage:.1f}%)"
        )


# Data quality section
st.header("Data quality")

st.markdown(
    """
    Basic validation checks were applied to identify reports
    with missing key fields or invalid seriousness codes.
    """
)

quality_col1, quality_col2 = st.columns(2)

with quality_col1:
    missing_count = reports["missing_key_data"].sum()
    st.metric(
        "Reports with missing key data",
        int(missing_count)
    )

with quality_col2:
    invalid_count = reports["invalid_serious_code"].sum()
    st.metric(
        "Reports with invalid seriousness codes",
        int(invalid_count)
    )

st.caption(
    "These checks cover selected fields and validation rules only; "
    "they do not represent a comprehensive assessment of report quality."
)


# Review prioritisation section
st.header("Review prioritisation")

st.markdown(
    """
    A transparent set of prototype rules was applied to identify
    selected reports for potential human review. These rules are
    illustrative and have not been clinically validated.
    """
)

reason_counts = pd.Series({
    "Selected event term": reports["selected_event_term"].sum(),
    "Missing key data": reports["missing_key_data"].sum(),
    "Invalid seriousness code": reports["invalid_serious_code"].sum()
})

reason_counts = reason_counts[reason_counts > 0]

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Reasons for review flags")
    st.bar_chart(reason_counts)

with col2:
    st.subheader("Flag summary")
    st.metric(
        "Reports flagged",
        int(reports["review_required"].sum())
    )
    st.caption(
        "A report may have more than one reason for being flagged. "
        "Reason counts are therefore not necessarily unique reports."
    )


# Reaction analysis section
st.header("Reaction analysis")

st.markdown(
    """
    Reaction terms are explored at the individual reaction-record
    level. The categories shown are illustrative analytical
    groupings, not validated MedDRA classifications.
    """
)

st.subheader("Reaction categories")

category_counts = reactions["reaction_category"].value_counts()

st.bar_chart(category_counts)

st.caption(
    "A large proportion of terms remain unclassified because "
    "the category mapping is deliberately limited. "
    "Unclassified does not mean that a report requires review."
)

st.divider()


# Most frequently reported reaction terms
st.subheader("Most frequently reported reaction terms")

top_reactions = (
    reactions["reaction_term"]
    .value_counts()
    .head(15)
)

st.bar_chart(top_reactions)


# Report explorer
st.header("Report explorer")

st.markdown(
    "Use the filters below to explore the available adverse-event reports."
)

explorer_reports = reports.copy()

explorer_reports["seriousness_label"] = (
    explorer_reports["serious"]
    .map({
        1: "Serious",
        2: "Not classified as serious"
    })
    .fillna("Unknown")
)

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    seriousness_filter = st.selectbox(
        "Report seriousness",
        [
            "All",
            "Serious",
            "Not classified as serious",
            "Unknown"
        ]
    )

with filter_col2:
    review_filter = st.selectbox(
        "Review status",
        [
            "All",
            "Flagged for review",
            "Not flagged"
        ]
    )


# Apply filters
filtered_reports = explorer_reports.copy()

if seriousness_filter != "All":
    filtered_reports = filtered_reports[
        filtered_reports["seriousness_label"] == seriousness_filter
    ]

if review_filter == "Flagged for review":
    filtered_reports = filtered_reports[
        filtered_reports["review_required"] == True
    ]

elif review_filter == "Not flagged":
    filtered_reports = filtered_reports[
        filtered_reports["review_required"] == False
    ]

st.write(f"**Reports matching filters: {len(filtered_reports):,}**")

display_columns = [
    "report_id",
    "receivedate",
    "seriousness_label",
    "review_required",
    "reaction_terms",
    "drug_names"
]

st.dataframe(
    filtered_reports[display_columns],
    use_container_width=True,
    hide_index=True
)


# Interpretation and limitations
st.header("Interpretation and limitations")

st.markdown(
    """
    This prototype uses publicly available FDA adverse-event
    reporting data to demonstrate data preparation, quality
    validation, rules-based review prioritisation and exploratory
    reaction analysis.

    **Important limitations**

    - Spontaneous reports do not establish a causal relationship
      between a drug and an adverse event.
    - Report counts cannot be used to estimate the incidence or
      probability of an adverse reaction.
    - Review flags are based on selected illustrative rules and
      are not validated pharmacovigilance triage criteria.
    - Reaction categories are limited analytical groupings and
      do not represent comprehensive or validated MedDRA coding.
    - Missing information in a report should not automatically
      be interpreted as evidence that an event did not occur.

    **Intended use:** An exploratory analytics and review-support
    prototype for demonstrating data quality assessment and
    transparent analytical methods. It is not a validated
    pharmacovigilance system or a substitute for expert review.
    """
)

st.divider()

st.caption(
    "Data source: FDA openFDA Adverse Event Reporting System (FAERS). "
    "Portfolio project for demonstration and educational purposes."
)
