"""
preprocess_job_data.py

Preprocesses the raw Kaggle "India Tech Jobs 2024-2026" dataset for the
Power BI "Job Market Skill Demand" dashboard.

WHAT THIS DOES:
1. Loads the raw dataset (5,000 postings across all tech roles)
2. Filters down to roles relevant to a data-analytics career path:
   Data Analyst, Data Scientist, Business Analyst, Data Engineer
3. Reshapes the comma-separated Skills_Required column into a "long"
   format (one row per job-skill pair) so Power BI can easily aggregate
   by individual skill.

HOW TO RUN:
    python preprocess_job_data.py
(Expects the raw Kaggle CSV — india_job_market_2024_2026.csv — in the
same folder.)

OUTPUT:
    job_postings.csv          — filtered, wide-format postings
    skills_long_format.csv    — filtered, long-format (job, skill) pairs
"""

import pandas as pd

RAW_FILE = "india_job_market_2024_2026.csv"
RELEVANT_TITLES = ["Data Analyst", "Data Scientist", "Business Analyst", "Data Engineer"]


def load_and_filter(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    filtered = df[df["Job_Title"].isin(RELEVANT_TITLES)].copy()
    print(f"Loaded {len(df)} total postings; filtered to {len(filtered)} "
          f"relevant to a data-analytics career path.")
    return filtered


def reshape_to_long_format(filtered: pd.DataFrame) -> pd.DataFrame:
    """
    Skills_Required looks like: "SQL, Tableau, Power BI, Statistics"
    This turns each posting into multiple rows — one per individual skill —
    which is far easier to aggregate ("how many postings mention SQL?")
    than parsing a comma-separated string inside Power BI/DAX.
    """
    rows = []
    for _, row in filtered.iterrows():
        skills = [s.strip() for s in row["Skills_Required"].split(",")]
        for skill in skills:
            rows.append({
                "Job_ID": row["Job_ID"],
                "skill": skill,
                "Job_Title": row["Job_Title"],
                "City": row["City"],
                "Location_Tier": row["Location_Tier"],
                "Experience_Level": row["Experience_Level"],
                "Work_Mode": row["Work_Mode"],
                "Salary_LPA": row["Salary_LPA"],
                "Date_Posted": row["Date_Posted"],
            })
    long_df = pd.DataFrame(rows)
    print(f"Reshaped into {len(long_df)} (job, skill) rows across "
          f"{long_df['skill'].nunique()} unique skills.")
    return long_df


def main():
    filtered = load_and_filter(RAW_FILE)
    filtered.to_csv("job_postings.csv", index=False)
    print("Saved job_postings.csv")

    long_df = reshape_to_long_format(filtered)
    long_df.to_csv("skills_long_format.csv", index=False)
    print("Saved skills_long_format.csv")

    print("\nTop 10 skills by number of postings mentioning them:")
    top_skills = long_df.groupby("skill")["Job_ID"].nunique().sort_values(ascending=False)
    print(top_skills.head(10))


if __name__ == "__main__":
    main()
