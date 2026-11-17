-- attrition_queries.sql
-- Run against cleaned_hr_data.csv loaded into a table named `employees`
-- (columns: employee_id, department, age, tenure_years, monthly_salary,
--  performance_rating, job_satisfaction, overtime, distance_from_home_km,
--  num_companies_worked, training_sessions_last_year, attrition)

-- 1. Overall attrition rate
SELECT
    ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM employees;

-- 2. Attrition rate by department
SELECT
    department,
    COUNT(*) AS total_employees,
    SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS left_company,
    ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY department
ORDER BY attrition_rate_pct DESC;

-- 3. Attrition rate by tenure bucket
SELECT
    CASE
        WHEN tenure_years < 2 THEN '<2 yrs'
        WHEN tenure_years < 5 THEN '2-5 yrs'
        WHEN tenure_years < 10 THEN '5-10 yrs'
        ELSE '10+ yrs'
    END AS tenure_bucket,
    COUNT(*) AS total_employees,
    ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY tenure_bucket
ORDER BY attrition_rate_pct DESC;

-- 4. Attrition rate by salary band
SELECT
    CASE
        WHEN monthly_salary < 45000 THEN 'Low'
        WHEN monthly_salary < 75000 THEN 'Mid'
        ELSE 'High'
    END AS salary_band,
    COUNT(*) AS total_employees,
    ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY salary_band
ORDER BY attrition_rate_pct DESC;

-- 5. Attrition rate by overtime status
SELECT
    overtime,
    COUNT(*) AS total_employees,
    ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
FROM employees
GROUP BY overtime;

-- 6. Average job satisfaction: left vs stayed
SELECT
    attrition,
    ROUND(AVG(job_satisfaction), 2) AS avg_job_satisfaction,
    ROUND(AVG(performance_rating), 2) AS avg_performance_rating
FROM employees
GROUP BY attrition;

-- 7. Top 10 highest-risk profiles (low tenure + low satisfaction + overtime)
SELECT employee_id, department, tenure_years, job_satisfaction, overtime, monthly_salary
FROM employees
WHERE tenure_years < 2 AND job_satisfaction <= 2 AND overtime = 'Yes'
ORDER BY tenure_years ASC
LIMIT 10;

-- 8. Department-wise average tenure of employees who left
SELECT
    department,
    ROUND(AVG(tenure_years), 1) AS avg_tenure_of_leavers
FROM employees
WHERE attrition = 'Yes'
GROUP BY department
ORDER BY avg_tenure_of_leavers ASC;

-- 9. Ranking departments by attrition rate using a window function
SELECT
    department,
    attrition_rate_pct,
    RANK() OVER (ORDER BY attrition_rate_pct DESC) AS attrition_rank
FROM (
    SELECT
        department,
        ROUND(100.0 * SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS attrition_rate_pct
    FROM employees
    GROUP BY department
) dept_summary;
