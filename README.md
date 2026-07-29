# 📊 Job Market Skill Demand Dashboard (Power BI)

![Dashboard Screenshot](dashboard_screenshot.png)


A Power BI dashboard analyzing **853 real Data Analyst / Data Scientist /
Business Analyst / Data Engineer job postings** in India (filtered from the
Kaggle dataset **"India Tech Jobs 2024-2026"** by Sridip Basu, which is
itself calibrated against real Naukri Salary Trends and AmbitionBox data).
The dashboard identifies the most in-demand skills in the market and
compares them against your own resume skillset to surface a **personal
skill gap analysis**.

**Why this project is different:** Most candidates build a generic
"Superstore Sales" or "Netflix" dashboard from an overused template. This
project uses a real, current job-market dataset to answer a genuinely
personal question — "what skills does the market actually want, and where
do I stand?" — which gives you a much stronger interview story than a
templated dashboard.

---

## Data Source (Fully Real — No Synthetic Data)

**Source:** Kaggle — "India Tech Jobs 2024-2026 | Salary & Skills" by Sridip Basu
**Original size:** 5,000 job postings across all tech roles
**Filtered for this project:** 853 postings, keeping only 4 roles relevant
to a data analytics career path: `Data Analyst`, `Data Scientist`,
`Business Analyst`, `Data Engineer`

---

## Files in This Project

| File | Description |
|------|--------------|
| `job_postings.csv` | 853 filtered postings — one row per posting, with all original columns (company, city, salary, skills, experience level, etc.) |
| `skills_long_format.csv` | Same data "unpivoted" — one row per (job, skill) pair — 3,826 rows. Makes skill-level visuals much easier to build. |
| `my_skills.csv` | Your resume skills tagged Yes/No against the 22 skills that actually appear in this dataset — used for the gap-analysis visual |

### Column Reference (`job_postings.csv`)

| Column | Description |
|--------|--------------|
| `Job_ID` | Unique posting ID |
| `Job_Title` | Data Analyst / Data Scientist / Business Analyst / Data Engineer |
| `Company`, `Company_Type`, `Industry`, `Company_Rating` | Employer info |
| `City`, `Location_Tier` | City name and Tier 1/Tier 2/Remote |
| `Experience_Level` | Fresher (0-1 yr) through Lead (10+ yrs) |
| `Job_Type`, `Work_Mode` | Full-Time/etc., Remote/Hybrid/On-Site |
| `Salary_LPA` | Salary in Lakhs Per Annum |
| `Skills_Required` | Comma-separated skill list (raw) |
| `Education_Required` | Degree requirement |
| `Openings`, `Applicants` | Posting-level hiring stats |
| `Date_Posted` | Posting date |

---

## Step 1: Import Data into Power BI

1. Open Power BI Desktop → **Get Data → Text/CSV**
2. Import `job_postings.csv` and `skills_long_format.csv` as two tables
3. In **Power Query Editor**, fix data types:
   - `Date_Posted` → Date
   - `Salary_LPA` → Decimal Number
   - `Openings`, `Applicants`, `Company_Rating` → Whole/Decimal Number
4. Import `my_skills.csv` as a third table

---

## Step 2: Create Relationships

In **Model View**:
- `job_postings[Job_ID]` → `skills_long_format[Job_ID]` (One-to-Many)

`my_skills` stays standalone — used via `LOOKUPVALUE` in Step 4.

---

## Step 3: Key DAX Measures

```dax
Total Job Postings = DISTINCTCOUNT(job_postings[Job_ID])
```

```dax
Total Unique Skills = DISTINCTCOUNT(skills_long_format[skill])
```

```dax
Skill Demand % =
DIVIDE(
    DISTINCTCOUNT(skills_long_format[Job_ID]),
    [Total Job Postings]
)
```
*(Drop `skill` on Rows of a bar chart/table with this measure as Values —
gives you % of postings mentioning each skill.)*

```dax
Avg Salary (LPA) = AVERAGE(job_postings[Salary_LPA])
```

```dax
Avg Applicants per Posting = AVERAGE(job_postings[Applicants])
```

```dax
Avg Openings per Posting = AVERAGE(job_postings[Openings])
```

---

## Step 4: Skill Gap Analysis (signature visual)

```dax
Skill Gap Table =
ADDCOLUMNS(
    SUMMARIZE(skills_long_format, skills_long_format[skill]),
    "Market Demand %",
        DIVIDE(
            CALCULATE(DISTINCTCOUNT(skills_long_format[Job_ID])),
            [Total Job Postings]
        ),
    "I Have This Skill",
        LOOKUPVALUE(my_skills[have_it], my_skills[skill], skills_long_format[skill])
)
```

Build a table/matrix visual from this calculated table:
- Rows: `skill`, sorted by `Market Demand %` descending
- Conditional formatting: green background where `I Have This Skill = "Yes"`,
  red/orange where `"No"` — these red rows are your priority learning list.

---

## Step 5: Recommended Dashboard Layout

**Row 1 — KPI Cards:**
- Total Job Postings (853)
- Total Unique Skills (22)
- Avg Salary (LPA)
- Avg Applicants per Posting (shows competitiveness)

**Row 2:**
- **Bar chart** — Top skills by `Skill Demand %` (headline visual)
- **Skill Gap matrix** (from Step 4) — side by side

**Row 3:**
- **Map visual** — postings by `City` (use Power BI's Map/Filled Map visual)
- **Matrix** — Top 3 skills per `Job_Title` (shows Data Analyst vs Data
  Scientist vs Data Engineer vs Business Analyst need very different skills)

**Row 4:**
- **Clustered bar** — Avg `Salary_LPA` by `Experience_Level`
- **Bar/Donut** — postings by `Work_Mode` (Remote/Hybrid/On-Site) and by
  `Location_Tier`

**Slicers (top of page):** `Job_Title`, `City`, `Experience_Level`, `Work_Mode`

---

## Real Insights Already Found in This Data
*(Use these directly in your dashboard commentary and interview answers —
these are the actual, verified numbers from the real dataset.)*

- **SQL is the single most in-demand skill — appears in 59% of all 853
  postings**, far ahead of anything else. Python (39%), Power BI (37%),
  Excel (36%), and Statistics (34%) round out the top 5.
- **Each role wants a genuinely different skillset:**
  - *Business Analyst* → Agile, Excel, Power BI
  - *Data Analyst* → Data Visualization, Power BI, Statistics
  - *Data Engineer* → dbt, Spark, Airflow
  - *Data Scientist* → Statistics, NLP, TensorFlow
- **Experience distribution:** Mid-level (3-6 yrs) postings are most common
  (234), but Fresher (0-1 yr) still accounts for 165 postings — a healthy
  entry-level market.
- **Remote is the single largest "location"** — 340 of 853 postings (40%)
  are Remote, ahead of any individual city (Pune and Hyderabad tied next
  at 70 each).
- Interestingly, in this dataset, postings that mention a niche/cloud skill
  (AWS, Spark, Kafka, Airflow, dbt, TensorFlow) show only a **marginally
  higher average salary (₹21.0 LPA vs ₹20.3 LPA)** — a more nuanced,
  honest finding than "cloud skills always pay dramatically more." Worth
  mentioning in an interview as evidence you interpret data honestly
  rather than forcing a dramatic conclusion that isn't really there.

---

## Interview Talking Points

**"Why did you build this?"**
"While applying for data analytics roles, I wanted actual evidence of what
skills recruiters were asking for instead of guessing. I used a real
Kaggle dataset of Indian tech job postings, filtered it to data-analytics-
relevant roles, and compared the market demand against my own resume to
prioritize what to learn next."

**"What was the most interesting insight?"**
"SQL alone appears in 59% of postings — more than any other skill by a
wide margin — which confirmed it's a genuinely non-negotiable skill,
not just something every course tells you. I also found each role wants a
different skillset — Data Engineers want Spark/Airflow/dbt while Data
Scientists want Statistics/NLP/TensorFlow — which helped me realize 'data
analytics' isn't one skillset, it's several adjacent but distinct ones."

**"Was the salary vs. skill relationship what you expected?"**
"Not entirely — I expected niche/cloud skills to show a much bigger salary
premium, but in this dataset the difference was small (₹21.0 vs ₹20.3 LPA).
I didn't force a bigger story than what the data actually showed — that
felt like an important discipline to practice."

**"How did you get the data?"**
"I downloaded a public Kaggle dataset of Indian tech job postings
calibrated against real Naukri/AmbitionBox salary data, then filtered it
down from 5,000 postings across all tech roles to the 853 relevant to a
data analytics career path."

**"What would you improve?"**
"I'd love to re-run this analysis periodically (e.g., quarterly) to see
how skill demand shifts over time, and combine it with a text-parsing
script to auto-extract skills from raw job descriptions rather than
relying on a pre-cleaned skills column."

---

## Optional Extension

To make this a combined Python + Power BI story, you could preprocess the
raw Kaggle CSV yourself in Python/Pandas (filtering job titles, splitting
the `Skills_Required` column into the long format) instead of using the
already-prepared `skills_long_format.csv` — then explain: "I used Python
to filter and reshape the raw dataset, then Power BI to model and
visualize it." This mirrors exactly what was done to prepare these files,
so you can walk through the real preprocessing logic if asked.
