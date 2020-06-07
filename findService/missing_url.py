import psycopg2
import logging
import datetime
from findService.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, MAILGUN_KEY, API, FROM_EMAIL, ADMIN
from findApp.parsing import *
import requests

today = datetime.date.today()
SUBJECT = 'Недостающие urls {}'.format(today)

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, "carModel_id" FROM subscribers_subscriber WHERE is_activ=%s;""", (True,))
    qs = cur.fetchall()
    cur.execute("""SELECT * FROM "findApp_city";""")
    cities_qs = cur.fetchall()
    cities = {i[0]: i[1] for i in cities_qs}
    cur.execute("""SELECT * FROM "findApp_carmodel";""")
    car_models_qs = cur.fetchall()
    car_models = {i[0]: i[1] for i in car_models_qs}
    mis_urls = []
    cnt = f'На {today} отсутствуют urls для:'
    for pair in qs:
        cur.execute("""SELECT * FROM "findApp_url" 
                WHERE city_id=%s AND "carModel_id"=%s;""", (pair[0], pair[1]))
        qs = cur.fetchall()
        if not qs:
            mis_urls.apppend((cities[pair[0]], car_models[1]))

    if mis_urls:
        for i in mis_urls:
            cnt += f'{i[0]} - {i[1]}'
            requests.post(API,
                auth=("api", MAILGUN_KEY),
                data={"from": FROM_EMAIL,
                      "to": ADMIN,
                      "subject": SUBJECT,
                      "text": cnt})

    conn.commit()
    cur.close()
    conn.close()