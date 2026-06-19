import pandas as pd
from loguru import logger
from sqlalchemy import create_engine
import os

def load():
    logger.info("Starting data load into PostgreSQL...")

    # Load cleaned data
    cleaned_path = 'data/processed/cleaned_jobs.csv'
    if not os.path.exists(cleaned_path):
        logger.error("Cleaned data not found. Run transform.py first.")
        raise FileNotFoundError("Cleaned data not found.")

    df = pd.read_csv(cleaned_path)
    logger.info(f"Loaded {len(df)} rows to push to PostgreSQL")

    # Connect to PostgreSQL
    # Replace 'yourpassword' with your actual PostgreSQL password
    try:
        engine = create_engine(
            'postgresql://postgres:postgres123@localhost:5432/ai_jobs_db'
        )
        logger.info("Connected to PostgreSQL successfully")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise

    # Load into PostgreSQL
    try:
        df.to_sql(
            'ai_jobs',
            engine,
            if_exists='replace',
            index=False
        )
        logger.info(f"Loaded {len(df)} rows into ai_jobs table")
    except Exception as e:
        logger.error(f"Data load failed: {e}")
        raise

    # Verify load
    result = pd.read_sql('SELECT COUNT(*) as total FROM ai_jobs', engine)
    total = result['total'][0]
    logger.info(f"Verified: {total} rows in database")

    return total

if __name__ == "__main__":
    total = load()
    print(f"Successfully loaded {total} rows into PostgreSQL")