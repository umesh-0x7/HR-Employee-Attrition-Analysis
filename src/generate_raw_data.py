"""
generate_raw_data.py
---------------------
Generates a synthetic (but realistic) HR employee dataset with attrition
outcomes correlated to tenure, salary, performance, and department -
then deliberately messes it up (duplicates, missing values, inconsistent
text, bad entries) to simulate a raw HR export.
"""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 1500

departments = ["Sales", "Engineering", "HR", "Marketing", "Finance", "Operations"]
dept_weights = [0.22, 0.28, 0.10, 0.15, 0.12, 0.13]

performance_ratings = [1, 2, 3, 4, 5]

def generate_employees(n):
    rows = []
    for i in range(1, n + 1):
        dept = np.random.choice(departments, p=dept_weights)
        tenure_years = round(np.random.exponential(scale=3.5), 1)
        tenure_years = min(tenure_years, 25)

        age = int(np.clip(np.random.normal(34, 8), 21, 60))

        performance = np.random.choice(performance_ratings, p=[0.05, 0.15, 0.40, 0.30, 0.10])

        base_salary = {
            "Sales": 55000, "Engineering": 85000, "HR": 50000,
            "Marketing": 58000, "Finance": 70000, "Operations": 52000
        }[dept]
        salary = int(base_salary + tenure_years * 1800 + np.random.normal(0, 6000))
        salary = max(salary, 28000)

        satisfaction = np.random.randint(1, 5)  # 1-4 job satisfaction survey score
        overtime = np.random.choice(["Yes", "No"], p=[0.30, 0.70])
        distance_from_home = np.random.randint(1, 40)
        num_companies_worked = np.random.randint(0, 7)
        training_last_year = np.random.randint(0, 6)

        # Attrition probability logic: higher risk with low tenure, low salary,
        # low satisfaction, overtime, low performance, long commute
        risk = 0
        risk += 0.35 if tenure_years < 2 else 0
        risk += 0.20 if satisfaction <= 2 else 0
        risk += 0.15 if overtime == "Yes" else 0
        risk += 0.15 if salary < base_salary else 0
        risk += 0.10 if distance_from_home > 25 else 0
        risk += 0.10 if performance <= 2 else 0
        risk -= 0.10 if tenure_years > 8 else 0

        attrition = "Yes" if np.random.rand() < np.clip(risk, 0.03, 0.9) else "No"

        rows.append({
            "employee_id": f"EMP{i:05d}",
            "department": dept,
            "age": age,
            "tenure_years": tenure_years,
            "monthly_salary": salary,
            "performance_rating": performance,
            "job_satisfaction": satisfaction,
            "overtime": overtime,
            "distance_from_home_km": distance_from_home,
            "num_companies_worked": num_companies_worked,
            "training_sessions_last_year": training_last_year,
            "attrition": attrition,
        })
    return pd.DataFrame(rows)


def mess_up_data(df):
    df = df.copy()

    # 1. Inconsistent text casing / whitespace in department
    def mess_dept(x):
        r = np.random.rand()
        if r < 0.15:
            return f"  {x.lower()} "
        elif r < 0.25:
            return x.upper()
        return x
    df["department"] = df["department"].apply(mess_dept)

    # 2. Duplicate ~30 rows (simulate export running twice)
    dup_rows = df.sample(30, random_state=1)
    df = pd.concat([df, dup_rows], ignore_index=True)

    # 3. Missing values in a few columns
    for col, frac in [("monthly_salary", 0.03), ("job_satisfaction", 0.04),
                       ("performance_rating", 0.03), ("overtime", 0.02)]:
        idx = df.sample(frac=frac, random_state=2).index
        df.loc[idx, col] = np.nan

    # 4. A few negative / impossible entries (data-entry errors)
    bad_idx = df.sample(8, random_state=3).index
    df.loc[bad_idx, "tenure_years"] = -df.loc[bad_idx, "tenure_years"]

    bad_idx2 = df.sample(5, random_state=4).index
    df.loc[bad_idx2, "age"] = 0

    # 5. Inconsistent Yes/No casing in overtime
    def mess_overtime(x):
        if pd.isna(x):
            return x
        r = np.random.rand()
        if r < 0.2:
            return x.lower()
        return x
    df["overtime"] = df["overtime"].apply(mess_overtime)

    # Shuffle rows so duplicates aren't neatly at the end
    df = df.sample(frac=1, random_state=5).reset_index(drop=True)
    return df


if __name__ == "__main__":
    clean = generate_employees(N)
    raw = mess_up_data(clean)
    raw.to_csv("data/raw_hr_data.csv", index=False)
    print(f"Generated {len(raw)} raw rows -> data/raw_hr_data.csv")
