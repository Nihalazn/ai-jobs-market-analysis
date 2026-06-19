import pandas as pd
from loguru import logger
from datetime import datetime
import os

def extract():
    logger.info("Starting data extraction...")
    
    # Path to raw data
    raw_path = 'data/raw/ai_job_dataset1.csv'
    
    # Check file exists
    if not os.path.exists(raw_path):
        logger.error(f"Raw data file not found: {raw_path}")
        raise FileNotFoundError(f"Raw data file not found: {raw_path}")
    
    # Load raw data
    df = pd.read_csv(raw_path)
    logger.info(f"Extracted {len(df)} rows from {raw_path}")
    
    # Add extraction timestamp
    df['extracted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Save to a staging area
    staging_path = 'data/processed/staging.csv'
    df.to_csv(staging_path, index=False)
    logger.info(f"Staged data saved to {staging_path}")
    
    return df

if __name__ == "__main__":
    df = extract()
    print(df.head())
    print(f"Shape: {df.shape}")