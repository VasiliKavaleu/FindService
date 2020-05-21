import psycopg2
import logging
import datetime
from findService.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

today = datetime.date.today()
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, carModel_id FROM subscribers_subscriber WHERE is_active=%s;""", (True,))
    cities_qs = cur.fetchall()
    print(cities_qs)

    conn.commit()
    cur.close()
    conn.close()