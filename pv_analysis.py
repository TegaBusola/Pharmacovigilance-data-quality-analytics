import pandas as pd


def flag_reports_for_review(df):
    """Flag reports for review using transparent, rule-based checks."""

    pv_review_df = df.copy()

    pv_review_df["serious_code"] = pd.to_numeric(
        pv_review_df["serious"], errors="coerce"
    )

    required_fields = [
        "report_id",
        "receivedate",
        "serious",
        "reaction_terms",
        "drug_names"
    ]

    pv_review_df["missing_key_data"] = False

    for column in required_fields:
        missing = (
            pv_review_df[column].isna()
            | pv_review_df[column]
                .astype("string")
                .str.strip()
                .eq("")
                .fillna(True)
        )
        pv_review_df["missing_key_data"] |= missing

    pv_review_df["invalid_serious_code"] = (
        pv_review_df["serious_code"].notna()
        & ~pv_review_df["serious_code"].isin([1, 2])
    )

    review_pattern = (
        r"\b(?:death|overdose|drug ineffective|"
        r"drug administration error|unevaluable event)\b"
    )

    pv_review_df["selected_event_term"] = (
        pv_review_df["reaction_terms"]
        .fillna("")
        .str.contains(review_pattern, case=False, regex=True)
    )

    def get_review_reasons(row):
        reasons = []

        if row["selected_event_term"]:
            reasons.append("Selected event term")

        if row["missing_key_data"]:
            reasons.append("Missing key data")

        if row["invalid_serious_code"]:
            reasons.append("Invalid seriousness code")

        return reasons

    pv_review_df["review_reasons"] = pv_review_df.apply(
        get_review_reasons, axis=1
    )

    pv_review_df["review_required"] = (
        pv_review_df["review_reasons"].str.len() > 0
    )

    return pv_review_df

def categorise_reaction_terms(reaction_df):
    """Apply transparent, rule-based reaction term categories."""

    reaction_df = reaction_df.copy()

    category_mapping = {
        # Medication use and administration
        "DRUG ADMINISTRATION ERROR": "Medication use / administration",
        "OVERDOSE": "Medication use / administration",

        # Treatment effectiveness
        "DRUG INEFFECTIVE": "Treatment effectiveness",

        # Patient outcomes
        "DEATH": "Patient outcomes",

        # Hypersensitivity
        "DRUG HYPERSENSITIVITY": "Hypersensitivity / allergic reactions",
        "ANGIOEDEMA": "Hypersensitivity / allergic reactions",

        # Injury and physical events
        "FALL": "Injury / physical events",
        "INJURY": "Injury / physical events",

        # General symptoms
        "DYSPNOEA": "General symptoms",
        "HEADACHE": "General symptoms",
        "FATIGUE": "General symptoms",
        "PAIN": "General symptoms",
        "DIARRHOEA": "General symptoms",
        "MALAISE": "General symptoms",
        "NAUSEA": "General symptoms",
        "INSOMNIA": "General symptoms",
        "DIZZINESS": "General symptoms",
        "ASTHENIA": "General symptoms",
        "VOMITING": "General symptoms",
        "PYREXIA": "General symptoms",
        "COUGH": "General symptoms",
        "TREMOR": "General symptoms",
        "ANXIETY": "General symptoms",
        "FEELING ABNORMAL": "General symptoms",
        "SOMNOLENCE": "General symptoms",

        # Clinical conditions and laboratory findings
        "TYPE 2 DIABETES MELLITUS": "Clinical conditions / laboratory findings",
        "ANAEMIA": "Clinical conditions / laboratory findings",
        "HAEMOGLOBIN DECREASED": "Clinical conditions / laboratory findings",
        "PNEUMONIA": "Clinical conditions / laboratory findings",
        "RENAL IMPAIRMENT": "Clinical conditions / laboratory findings",
        "HEPATIC ENZYME INCREASED": "Clinical conditions / laboratory findings",
    }

    reaction_df["reaction_category"] = (
        reaction_df["reaction_term"]
        .str.strip()
        .str.upper()
        .map(category_mapping)
        .fillna("Other / unclassified")
    )

    return reaction_df