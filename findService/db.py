import psycopg2
import logging
import datetime
from findService.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST
from findApp.parsing import *

today = datetime.date.today()
# some_days_age = datetime.date.today() - datetime.timedelta(20)
try:
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASSWORD)
except:
    logging.exception('Unable to open DB -{}'.format(today))
else:
    cur = conn.cursor()
    cur.execute("""SELECT city_id, "carModel_id" FROM subscribers_subscriber WHERE is_activ=%s;""", (True,))
    cities_qs = cur.fetchall()
    print(cities_qs)
    todo_list = { i[0]:set() for i in cities_qs}
    for i in cities_qs:
        todo_list[i[0]].add(i[1])
    print(todo_list)
    cur.execute("""SELECT * FROM "findApp_site";""")
    sites_qs = cur.fetchall()
    sites = {i[0]:i[1] for i in sites_qs}
    print(sites)
    url_list = []
    for city in todo_list:
        for model in todo_list[city]:
            tmp = {}
            cur.execute("""SELECT site_id, url_adress FROM "findApp_url" 
                    WHERE city_id=%s AND "carModel_id"=%s;""", (city, model))
            qs = cur.fetchall()
            print(qs)
            if qs:
                tmp['city'] = city
                tmp['carModel'] = model
                for item in qs:
                    site_id = item[0]
                    tmp[sites[site_id]] = item[1]
                url_list.append(tmp)
    print(url_list)
    all_data = []
    if url_list:
        for url in url_list:
            tmp = {}
            tmp_content = []
            tmp_content.extend(av(url['av.by']))
            tmp['city'] = url['city']
            tmp['carModel'] = url['carModel']
            tmp['content'] = tmp_content
            all_data.append(tmp)
    print("GET DATA")
    if all_data:
        for data in all_data:
            city = data['city']
            carModel = data['carModel']
            autos = data['content']
            for auto in autos:
                cur.execute("""SELECT * FROM "findApp_auto" 
                        WHERE url=%s;""", (auto['href'],))
                qs = cur.fetchone()
                if not qs:
                    cur.execute("""INSERT INTO "findApp_auto" ("carModel_id", title, url, description, 
                                price, city_id, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s); """,
                                (carModel, auto['name'], auto['href'], auto['desc'], auto['price'], city, today))
    # cur.execute("""DELETE FROM "findApp_Auto" WHERE timestamp<=%s;""", (some_days_age,))

    conn.commit()
    cur.close()
    conn.close()