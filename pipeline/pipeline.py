import sys
import os
from loguru import logger
from datetime import datetime

# Add pipeline folder to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from extract import extract
from transform import transform
from load import load

# Setup logging to file
log_file = f"logs/pipeline_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logger.add(log_file, rotation="1 day", retention="7 days")

def run_pipeline():
    logger.info("="*50)
    logger.info("PIPELINE STARTED")
    logger.info("="*50)

    try:
        logger.info("STEP 1: Extraction")
        df_raw = extract()
        logger.info(f"Extraction complete: {len(df_raw)} rows")

        logger.info("STEP 2: Transformation")
        df_clean = transform()
        logger.info(f"Transformation complete: {len(df_clean)} rows")

        logger.info("STEP 3: Loading")
        total = load()
        logger.info(f"Load complete: {total} rows in database")

        logger.info("="*50)
        logger.info("PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*50)

    except Exception as e:
        logger.error(f"PIPELINE FAILED: {e}")
        raise

if __name__ == "__main__":
    run_pipeline()