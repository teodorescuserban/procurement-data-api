#/usr/bin/python3

import config
import pymysql
import sys
import bas

if sys.argv[1]:
    notices = bas.load_tenders(sys.argv[1])
else:
    notices = bas.load_tenders(sys.stdin)

connection = pymysql.connect(
    host=config.DATABASE['hostname'],
    user=config.DATABASE['username'],
    password=config.DATABASE['password'],
    db=config.DATABASE['database'],
    charset='utf8'
)

with connection.cursor() as cursor:
    for refno in notices:
        notice = notices.get(refno)
        result = cursor.execute('insert into Tenders (tender, title_en, title_fr) values (%s, %s, %s) on duplicate key update title_en=values(title_en), title_fr=values(title_fr)', [refno, notice.title_en, notice.title_fr])
        print(result)

connection.commit()
