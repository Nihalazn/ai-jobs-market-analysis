-- 1. Total number of jobs
SELECT COUNT(*) AS total_jobs FROM ai_jobs;

-- 2. Average salary by experience level
SELECT experience_level,
       ROUND(AVG(salary_usd)) AS avg_salary,
       COUNT(*) AS job_count
FROM ai_jobs
GROUP BY experience_level
ORDER BY avg_salary DESC;

-- 3. Top 10 highest paying job titles
SELECT job_title,
       ROUND(AVG(salary_usd)) AS avg_salary,
       COUNT(*) AS job_count
FROM ai_jobs
GROUP BY job_title
ORDER BY avg_salary DESC
LIMIT 10;

-- 4. Average salary by industry
SELECT industry,
       ROUND(AVG(salary_usd)) AS avg_salary,
       COUNT(*) AS job_count
FROM ai_jobs
GROUP BY industry
ORDER BY avg_salary DESC;

-- 5. Salary by company size
SELECT company_size,
       ROUND(AVG(salary_usd)) AS avg_salary,
       ROUND(MIN(salary_usd)) AS min_salary,
       ROUND(MAX(salary_usd)) AS max_salary
FROM ai_jobs
GROUP BY company_size
ORDER BY avg_salary DESC;

-- 6. Remote vs onsite job count
SELECT remote_ratio,
       COUNT(*) AS job_count,
       ROUND(AVG(salary_usd)) AS avg_salary
FROM ai_jobs
GROUP BY remote_ratio
ORDER BY remote_ratio DESC;

-- 7. Top 5 countries with most AI jobs
SELECT company_location,
       COUNT(*) AS job_count,
       ROUND(AVG(salary_usd)) AS avg_salary
FROM ai_jobs
GROUP BY company_location
ORDER BY job_count DESC
LIMIT 5;

-- 8. Average salary by education level
SELECT education_required,
       ROUND(AVG(salary_usd)) AS avg_salary,
       COUNT(*) AS job_count
FROM ai_jobs
GROUP BY education_required
ORDER BY avg_salary DESC;

-- 9. Average salary by years of experience
SELECT years_experience,
       ROUND(AVG(salary_usd)) AS avg_salary,
       COUNT(*) AS job_count
FROM ai_jobs
GROUP BY years_experience
ORDER BY years_experience ASC;

-- 10. High paying entry level jobs (EN > $100k)
SELECT job_title,
       company_location,
       salary_usd,
       required_skills
FROM ai_jobs
WHERE experience_level = 'EN'
AND salary_usd > 100000
ORDER BY salary_usd DESC
LIMIT 10;