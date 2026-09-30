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