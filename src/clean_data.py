"""
clean_data.py
-------------
Cleans the raw HR export:
- standardizes text fields (department, overtime)
- removes duplicate employee records
- fixes impossible values (negative tenure, age = 0)
- imputes missing numeric values (median by department)
- imputes missing categorical values (mode)
"""

import numpy as np
import pandas as pd

def clean(df):
    df = df.copy()

    # Standardize text
    df["department"] = df["department"].str.strip().str.title()
    df["overtime"] = df["overtime"].str.strip().str.capitalize()

    # Remove duplicate employee records (keep first occurrence)
    before = len(df)
    df = df.drop_duplicates(subset="employee_id", keep="first")
    removed = before - len(df)

    # Fix impossible values
    df["tenure_years"] = df["tenure_years"].abs()
    df.loc[df["age"] == 0, "age"] = np.nan

    # Impute missing numeric values with median (by department where sensible)
    for col in ["monthly_salary", "job_satisfaction", "performance_rating", "age"]:
        df[col] = df.groupby("department")[col].transform(lambda s: s.fillna(s.median()))
        df[col] = df[col].fillna(df[col].median())  # catch any leftover NaNs

    # Impute missing categorical values with mode
    df["overtime"] = df["overtime"].fillna(df["overtime"].mode()[0])

    # Enforce sensible dtypes
    df["age"] = df["age"].round().astype(int)
    df["performance_rating"] = df["performance_rating"].round().astype(int)
    df["job_satisfaction"] = df["job_satisfaction"].round().astype(int)
    df["monthly_salary"] = df["monthly_salary"].round().astype(int)

    print(f"Removed {removed} duplicate rows. {len(df)} clean rows remain.")
    return df


if __name__ == "__main__":
    raw = pd.read_csv("data/raw_hr_data.csv")
    cleaned = clean(raw)
    cleaned.to_csv("data/cleaned_hr_data.csv", index=False)
    print("Saved -> data/cleaned_hr_data.csv")
