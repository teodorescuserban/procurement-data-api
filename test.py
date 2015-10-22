#/usr/bin/python3

import sys
import bas

if sys.argv[1]:
    notices = bas.load_tenders(sys.argv[1])
else:
    notices = bas.load_tenders(sys.stdin)

for refno in notices:
    print(notices.get(refno))
