import psycopg2
import logging
import datetime
from findService.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, MAILGUN_KEY, API, FROM_EMAIL
from findApp.parsing import *
import requests

today = datetime.date.today()


SUBJECT = 'Список авто за {}'.format(today)

template ='<!doctype html><html lang="en"><head><meta charset="utf-8"></head><body>'
end = '</body></html>'

try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, "carModel_id" FROM subscribers_subscriber WHERE is_activ=%s;""", (True,))
    cities_qs = cur.fetchall()
    for pair in cities_qs:
        content= ''
        city = pair[0]
        carModel = pair[1]
        cur.execute("""SELECT email FROM subscribers_subscriber WHERE is_activ=%s AND city_id=%s 
                        AND "carModel_id"=%s;""", (True, city, carModel))
        email_qs = cur.fetchall()
        emails = [i[0] for i in email_qs]
        cur.execute("""SELECT url, title, description, price FROM "findApp_auto" 
                        WHERE city_id=%s AND "carModel_id"=%s AND 
                        timestamp=%s;""", (city, carModel, today))
        autos_qs = cur.fetchall()
        if autos_qs:
            for auto in autos_qs:
                content += '<a href="{}" target="_blank">'.format(auto[0])
                content += '{}</a><br/>'.format(auto[1])
                content += '<p>{}</p>'.format(auto[2])
                content += '<p>{}</p>'.format(auto[3])
                content += '<hr/><br/><br/>'
            html_m = template + content + end
            for email in emails:
                requests.post(API,
                    auth=("api", MAILGUN_KEY),
                    data={"from": FROM_EMAIL,
                          "to": [email],
                          "subject": SUBJECT,
                          "html": html_m})
        else:
            for email in emails:
                print(email)
                requests.post(API,
                auth = ("api", MAILGUN_KEY),
                data = {"from": FROM_EMAIL,
                        "to": [email],
                        "subject": SUBJECT,
                        "text": "Список авто по Вашему профилю на сегодня пуст."})

    conn.commit()
    cur.close()
    conn.close()