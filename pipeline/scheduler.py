import sys
import os
from loguru import logger
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

# Add pipeline folder to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from pipeline import run_pipeline

# Setup logging
log_file = f"logs/scheduler_{datetime.now().strftime('%Y%m%d')}.log"
logger.add(log_file, rotation="1 day", retention="7 days")

def scheduled_job():
    logger.info(f"Scheduled run triggered at {datetime.now()}")
    try:
        run_pipeline()
        logger.info("Scheduled run completed successfully")
    except Exception as e:
        logger.error(f"Scheduled run failed: {e}")

if __name__ == "__main__":
    scheduler = BlockingScheduler()

    # Run every 24 hours
    scheduler.add_job(
        scheduled_job,
        'interval',
        hours=24,
        next_run_time=datetime.now()  # runs immediately first time
    )

    logger.info("Scheduler started — pipeline runs every 24 hours")
    logger.info("Press Ctrl+C to stop")

    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
        scheduler.shutdown()