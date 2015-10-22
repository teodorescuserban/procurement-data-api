"""Top-level module for BuyAndSell data."""

import bas.tender_notices
import pymysql

saved_connection = None

def load_tenders(source):
    return bas.tender_notices.TenderNoticeList.load(source)

def connect(config):
    """Get a database connection."""
    global saved_connection
    if not saved_connection:
        saved_connection = pymysql.connect(
            host=config.DATABASE['hostname'],
            user=config.DATABASE['username'],
            password=config.DATABASE['password'],
            db=config.DATABASE['database'],
            charset='utf8'
        )
    return saved_connection

