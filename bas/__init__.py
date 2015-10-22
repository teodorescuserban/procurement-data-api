
from bas.tender_notices import TenderNoticeList

def load_tenders(source):
    return TenderNoticeList.load(source)
