import pandas as pd
from loguru import logger
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def transform():
    logger.info("Starting data transformation...")

    # Load staged data
    staging_path = 'data/processed/staging.csv'
    if not os.path.exists(staging_path):
        logger.error("Staging file not found. Run extract.py first.")
        raise FileNotFoundError("Staging file not found.")

    df = pd.read_csv(staging_path)
    logger.info(f"Loaded {len(df)} rows from staging")

    # Drop unnecessary columns
    drop_cols = ['job_id', 'salary_local',
                 'salary_currency', 'extracted_at']
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])
    logger.info("Dropped unnecessary columns")

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Removed {before - len(df)} duplicate rows")

    # Remove salary outliers
    df = df[df['salary_usd'] > 5000]
    df = df[df['salary_usd'] < 500000]
    logger.info(f"Rows after salary filter: {len(df)}")

    # Group rare job titles
    title_counts = df['job_title'].value_counts()
    df['job_title_grouped'] = df['job_title'].apply(
        lambda x: x if title_counts[x] >= 50 else 'Other'
    )

    # Group rare locations
    loc_counts = df['company_location'].value_counts()
    df['location_grouped'] = df['company_location'].apply(
        lambda x: x if loc_counts[x] >= 50 else 'Other'
    )

    # Group rare residences
    res_counts = df['employee_residence'].value_counts()
    df['residence_grouped'] = df['employee_residence'].apply(
        lambda x: x if res_counts[x] >= 50 else 'Other'
    )

    # Group rare skills
    skill_counts = df['required_skills'].value_counts()
    df['skills_grouped'] = df['required_skills'].apply(
        lambda x: x if skill_counts[x] >= 50 else 'Other'
    )

    # Group rare industries
    ind_counts = df['industry'].value_counts()
    df['industry_grouped'] = df['industry'].apply(
        lambda x: x if ind_counts[x] >= 50 else 'Other'
    )

    logger.info("Grouped rare categories")

    # Load saved encoders and encode columns
    encoder_cols = [
        'salary_currency', 'experience_level',
        'employment_type', 'company_size',
        'job_title_grouped', 'location_grouped',
        'residence_grouped', 'skills_grouped',
        'industry_grouped', 'education_required'
    ]

    for col in encoder_cols:
        encoder_path = f'models/encoders/{col}_encoder.pkl'
        if os.path.exists(encoder_path):
            le = joblib.load(encoder_path)
            if col in df.columns:
                df[col] = df[col].apply(
                    lambda x: le.transform([x])[0]
                    if x in le.classes_ else -1
                )
            logger.info(f"Encoded {col}")

    # Save cleaned data
    output_path = 'data/processed/cleaned_jobs.csv'
    df.to_csv(output_path, index=False)
    logger.info(f"Transformed data saved: {df.shape[0]} rows")

    return df

if __name__ == "__main__":
    df = transform()
    print(df.head())
    print(f"Shape: {df.shape}")