"""Top-level module for BuyAndSell data."""

import bas.tender_notices

def load_tenders(source):
    return bas.tender_notices.TenderNoticeList.load(source)
