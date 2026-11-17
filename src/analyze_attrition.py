"""
analyze_attrition.py
---------------------
Exploratory analysis on the cleaned HR dataset:
- overall attrition rate
- attrition by department, tenure bucket, salary band, overtime
- generates charts into visuals/
- prints key insights to console
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (8, 5)


def tenure_bucket(years):
    if years < 2:
        return "<2 yrs"
    elif years < 5:
        return "2-5 yrs"
    elif years < 10:
        return "5-10 yrs"
    else:
        return "10+ yrs"


def salary_band(salary):
    if salary < 45000:
        return "Low"
    elif salary < 75000:
        return "Mid"
    else:
        return "High"


def main():
    df = pd.read_csv("data/cleaned_hr_data.csv")
    df["tenure_bucket"] = df["tenure_years"].apply(tenure_bucket)
    df["salary_band"] = df["monthly_salary"].apply(salary_band)
    df["attrition_flag"] = (df["attrition"] == "Yes").astype(int)

    overall_rate = df["attrition_flag"].mean() * 100
    print(f"Overall attrition rate: {overall_rate:.1f}%")

    # --- Attrition by department ---
    dept_rate = df.groupby("department")["attrition_flag"].mean().sort_values(ascending=False) * 100
    print("\nAttrition rate by department:")
    print(dept_rate.round(1))

    ax = dept_rate.plot(kind="bar", color="#4C72B0")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_title("Attrition Rate by Department")
    plt.tight_layout()
    plt.savefig("visuals/attrition_by_department.png", dpi=150)
    plt.close()

    # --- Attrition by tenure bucket ---
    order = ["<2 yrs", "2-5 yrs", "5-10 yrs", "10+ yrs"]
    tenure_rate = df.groupby("tenure_bucket")["attrition_flag"].mean().reindex(order) * 100
    print("\nAttrition rate by tenure bucket:")
    print(tenure_rate.round(1))

    ax = tenure_rate.plot(kind="bar", color="#DD8452")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_title("Attrition Rate by Tenure")
    plt.tight_layout()
    plt.savefig("visuals/attrition_by_tenure.png", dpi=150)
    plt.close()

    # --- Attrition by salary band ---
    band_order = ["Low", "Mid", "High"]
    salary_rate = df.groupby("salary_band")["attrition_flag"].mean().reindex(band_order) * 100
    print("\nAttrition rate by salary band:")
    print(salary_rate.round(1))

    ax = salary_rate.plot(kind="bar", color="#55A868")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_title("Attrition Rate by Salary Band")
    plt.tight_layout()
    plt.savefig("visuals/attrition_by_salary.png", dpi=150)
    plt.close()

    # --- Attrition by overtime ---
    ot_rate = df.groupby("overtime")["attrition_flag"].mean() * 100
    print("\nAttrition rate by overtime status:")
    print(ot_rate.round(1))

    fig, ax = plt.subplots()
    ax.pie(
        [overall_rate, 100 - overall_rate],
        labels=["Attrition", "Retained"],
        autopct="%1.1f%%",
        colors=["#C44E52", "#8FBFE0"],
        startangle=90,
    )
    ax.set_title("Overall Attrition Rate")
    plt.tight_layout()
    plt.savefig("visuals/attrition_rate_overview.png", dpi=150)
    plt.close()

    print("\nCharts saved to visuals/")


if __name__ == "__main__":
    main()
