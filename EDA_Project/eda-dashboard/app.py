import streamlit as st
import pandas as pd
from io import StringIO

#Cleaning function

def clean_data(df: pd.DataFrame) -> pd.DataFrame:

    cleaned_df = df.copy()

    # Clean text columns

    text_columns = [
        "job_title",
        "company",
        "location",
        "experience_level"
    ]

    for column in text_columns:
        cleaned_df[column] = (
            cleaned_df[column]
            .str.strip()
        )

    # Normalize experience levels

    cleaned_df["experience_level"] = (
        cleaned_df["experience_level"]
        .str.lower()
    )

    experience_mapping = {
        "jr": "junior",
        "entry": "junior",
        "entry level": "junior",
        "entry-level": "junior",
        "mid": "intermediate",
        "mid-level": "intermediate",
        "sr": "senior"
    }

    cleaned_df["experience_level"] = (
        cleaned_df["experience_level"]
        .replace(experience_mapping)
    )

    # Converting salary to numeric

    cleaned_df["salary"] = pd.to_numeric(
        cleaned_df["salary"],
        errors="coerce"
    )

    # Mark invalid salaries missing

    cleaned_df.loc[
        cleaned_df["salary"] <= 0,
        "salary"
    ] = pd.NA

    # Remove records without salary

    cleaned_df = cleaned_df.dropna(
        subset=["salary"]
    )

    # Remove duplicate records

    cleaned_df = cleaned_df.drop_duplicates()

    return cleaned_df

# Load dataset

raw_df = pd.read_csv(
    "data/software_jobs.csv"
)

df = clean_data(raw_df)

# page

st.title("Software jobs EDA dashboard")

st.write(
    "Exploratory data analysis of "
    "software development job postings."
)

# Original dataset inspection

with st.expander("Original Dataset Inspection"):

    st.subheader("Shape")

    st.write(
        "Rows:",
        raw_df.shape[0]
    )

    st.write(
        "Columns:",
        raw_df.shape[1]
    )

    st.subheader("Column Names")

    st.write(
        raw_df.columns.tolist()
    )

    st.subheader("First five records")

    st.dataframe(
        raw_df.head()
    )

    st.subheader("Last five records")

    st.dataframe(
        raw_df.tail()
    )

    st.subheader("Data types")

    st.write(
        raw_df.dtypes
    )

    st.subheader("DataFrame information")

    buffer = StringIO()

    raw_df.info(
        buf=buffer
    )

    st.text(
        buffer.getvalue()
    )

    st.subheader("Descriptive statistics")

    st.dataframe(
        raw_df.describe()
    )

    st.subheader("Missing values")

    st.write(
        raw_df.isna().sum()
    )

    st.subheader("Duplicated rows")

    st.write(
        raw_df.duplicated().sum()
    )

    duplicates = raw_df[
        raw_df.duplicated(
            keep=False
        )
    ]

# Cleaning summary

with st.expander("Data Cleaning summary"):

    raw_rows = len(raw_df)
    clean_rows = len(df)

    st.write(
        "Original rows:",
        raw_rows
    )

    st.write(
        "Clean rows:",
        clean_rows
    )

    st.write(
        "Rows removed:",
        raw_rows - clean_rows
    )

    st.subheader(
        "Remaining missing values"
    )

    st.write(
        df.isna().sum()
    )

    st.subheader(
        "Remaining duplicate rows"
    )

    st.write(
        df.duplicated().sum()
    )

    st.subheader(
        "Cleaned data types"
    )

    st.write(
        df.dtypes
    )

    st.subheader(
        "Experience levels"
    )

    st.write(
        df["experience_level"]
        .value_counts()
    )

    st.subheader(
        "Locations"
    )
    st.write(
        df["location"]
        .value_counts()
    )

# Clean dataset
st.subheader("Clean dataset")

st.dataframe(
    df,
    use_container_width=True
)

# Descriptive statistics

st.header("Descriptive Statistics")

salary_count = df["salary"].count()
salary_mean = df["salary"].mean()
salary_median = df["salary"].median()
salary_min = df["salary"].min()
salary_max = df["salary"].max()

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Salary records",
        f"${salary_count:,.0f}"
    )

with col2:
    st.metric(
        "Mean salary",
        f"${salary_mean:,.0f}"
    )

with col3:
    st.metric(
        "Median Salary",
        f"${salary_median:,.0f}"
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "Minimum Salary",
        f"${salary_min:,.0f}"
    )

with col5:
    st.metric(
        "Maximum Salary",
        f"${salary_max:,.0f}"
    )

salary_range = (
    salary_max - salary_min
)

st.metric(
    "Salary range",
    f"${salary_range:,.0f}"
)

salary_std = df["salary"].std()

st.metric(
    "Salary Standard Deviation",
    f"${salary_std:,.0f}"
)

salary_variance = df["salary"].var()

q1 = df["salary"].quantile(0.25)
q2 = df["salary"].quantile(0.50) # This one is the median
q3 = df["salary"].quantile(0.75)

st.subheader("Salary quartiles")

quartile_col1, quartile_col2, quartile_col3 = st.columns(3)

with quartile_col1:
    st.metric(
        "Q1 - 25th percentile",
        f"${q1:,.0f}"
    )
with quartile_col2:
    st.metric(
        "Q2 - Median",
        f"${q2:,.0f}"
    )

with quartile_col3:
    st.metric(
        "Q3 - 75th percentile",
        f"${q3:,.0f}"
    )

salary_mode = df["salary"].mode()

df["experience_level"].value_counts()

experience_counts = (
    df["experience_level"]
    .value_counts()
)

st.subheader(
    "Experience-level frequency"
)

st.dataframe(
    experience_counts
)

experience_proportions = (
    df["experience_level"]
    .value_counts(normalize=True)
)

experience_percentages = (
    df["experience_level"]
    .value_counts(normalize=True)
    * 100
)

experience_summary = pd.DataFrame({
    "count": df["experience_level"].value_counts(),
    "precentage": (
        df["experience_level"]
        .value_counts(normalize=True)
        * 100
    )
})

experience_summary["percentage"] = (
    experience_summary["percentage"]
    .round(1)
)

st.subheader(
    "Experience-level distribution"
)

st.dataframe(
    experience_summary
)

salary_by_experience = (
    df.groupby("experience_level")["salary"]
    .mean()
)

st.subheader(
    "Mean salary by experience level"
)

st.dataframe(
    salary_by_experience
)

salary_by_experience = (
    df
    .groupby("experience_level")["salary"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
)

salary_by_location = (
    df
    .groupby("location")["salary"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
)

st.subheader(
    "Salary by location"
)

st.dataframe(
    salary_by_location
)

remote_summary = (
    df
    .groupby("remote")["salary"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
)

st.subheader(
    "Salary by remote status"
)

st.dataframe(
    remote_summary
)

st.subheader(
    "Clean dataset statistical summary"
)

st.datagrame(
    df.describe()
)

def calculate_salary_statistics(
        df: pd.DataFrame
) -> dict:

    salary = df["salary"]

    return {
        "count": salary.count(),
        "mean": salary.mean(),
        "median": salary.median(),
        "minimum": salary.min(),
        "maximum": salary.max(),
        "range": (
            salary.max()
              - salary.min()
        ),
        "std": salary.std(),
        "variance": salary.var(),
        "q1": salary.quantile(0.25),
        "q3": salary.quantile(0.75),
        "iqr": q3 - q1
    }

salary_stats = (
    calculate_salary_statistics(df)
)

# Descriptive statistics

st.header("Descriptive statistics")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Salary records",
        f"{salary_stats['count']:,}"
    )

with col2:
    st.metric(
        "Mean salary",
        f"${salary_stats['mean']:,.0f}"
    )

with col3:
    st.metric(
        "Median salary",
        f"${salary_stats['median']:,.0f}"
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        "Minimum salary",
        f"${salary_stats['minimum']:,.0f}"
    )

with col5:
    st.metric(
        "Maximum salary",
        f"${salary_stats['maximum']:,.0f}"
    )

with col6:
    st.metric(
        "Salary range",
        f"${salary_stats['range']:,.0f}"
    )

col7, col8 = st.columns(2)

with col7:
    st.metric(
        "Standard deviation",
        f"${salary_stats['std']:,.0f}"
    )

with col8:
    st.metric(
        "Interquartile range",
        f"${salary_stats['iqr']:,.0f}"
    )

st.subheader(
    "Salary quartiles"
)

quartile_col1, quartile_col2, quartile_col3 = (
    st.columns(3)
)

with quartile_col1:
    st.metric(
        "Q1 - 25th percentile",
        f"F{salary_stats['q1']:,.0f}"
    )

with quartile_col2:
    st.metric(
        "Q2 - Median",
        f"${salary_stats['median']:,.0f}"
    )

with quartile_col3:
    st.metric(
        "Q3 - 75th percentile",
        f"${salary_stats['q3']:,.0f}"
    )

st.subheader(
    "Experience-level distribution"
)

experience_summary = pd.DataFrame({
    "count": (
        df["experience_level"]
        .value_counts()
    ),
    "percentage": (
        df["experience_level"]
        .value_counts(
            normalize=True
        )
        * 100
    )
})

experience_summary["percentage"] = (
    experience_summary["percentage"]
    .round(1)
)

st.dataframe(
    experience_summary,
    use_container_width=True
)

st.subheader(
    "Salary by experience level"
)

salary_by_experience = (
    df
    .groupby("experience_level")["salary"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max",
        "std"
    ])
    .round(2)
)

st.dataframe(
    salary_by_experience,
    use_container_width=True
)

st.subheader(
    "Salary by location"
)

salary_by_location = (
    df
    .groupby("location")["salary"]
    .agg([
        "count",
        "mean",
        "median",
        "min",
        "max"
    ])
    .round(2)
)

st.dataframe(
    salary_by_location,
    use_container_width=True
)
