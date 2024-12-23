import time

from flask import Flask, request, render_template
import requests, re
import psycopg2
from bs4 import BeautifulSoup

conn = psycopg2.connect(database="habrdb", user="etis", password="webreview", host="localhost", port=5432)
cur = conn.cursor()
app = Flask(__name__)
response = []
try:
    rs = (requests.get(
        'https://student.psu.ru/pls/stu_cus_et/tt_pkg.show_prep?P_TERM=&P_PEO_ID=&P_SDIV_ID=&P_TY_ID=2024&P_WDAY=&P_WEEK=17',
        timeout=30))
    response.append(rs)
except requests.exceptions.ConnectTimeout:
    print('FUCKINGTIMEOUT')
    time.sleep(15)

r_lec = [
    r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>старший преподаватель)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))',
    r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>преподаватель)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))',
    r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>Док.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))',
    r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>Кан.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))',
    r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>ассистент.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))']
r_left = r"(?P<Name>.*?\s+.*?\s+.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))"


@app.route('/start')
def hello_world():
    result = response[0].text
    lector = 'none'
    time_start = '0:00'
    numday = 0;
    for rr in response:
        if rr.text.find('8:00') != -1:
            soup = BeautifulSoup(rr.text, 'lxml')
            table = soup.find_all('table')[0]
            result += rr.text
            headers = []
            rows = []
            for j, row in enumerate(table.find_all('tr')):
                if j == 0:
                    headers = [el.text.strip() for el in row.find_all('th')]
                else:
                    rows.append([el.text.strip() for el in row.find_all('td')])
            for row in rows:
                size = len(row)
                for item in row:
                    if item == '':
                        numday += 1
                        continue
                    if item[2] != ':' and item[1] != ':':
                        if re.match(r_left, item) is not None:
                            lector = item
                            for reg in r_lec:
                                try:
                                    if re.match(reg, lector) is not None:
                                        lc = re.split(reg, lector)
                                    else:
                                        continue
                                    lector = lc[1]
                                except:
                                    continue
                        else:
                            numday += 1
                            tblrs = item.split('\n')
                            if tblrs[0] == "Нет занятий":
                                continue
                            else:
                                subject = tblrs[0]
                                auditory = tblrs[1]
                                for tblr in tblrs:
                                    if re.match(r'[А-ЯёЁ]+/[А-ЯёЁ]\s.*?\d+-20\d\d\s[А-ЯёЁ]{2}', tblr) is not None:
                                        insert_query = '''INSERT INTO tabs (studs, lector, time, aud, sub, day) VALUES (%s, %s, %s, %s, %s, %s)'''
                                        item_tuple = (tblr, lector, time_start, auditory, subject, numday)
                                        cur.execute(insert_query, item_tuple)
                                        item_tuple = (tblr,)
                                        insert_query = '''INSERT INTO studs (studs) VALUES (%s)'''
                                        cur.execute(insert_query, item_tuple)

                                    else:
                                        continue

                    else:
                        time_start = item
                        numday = 0;

                    continue
    sql1 = '''SELECT * FROM tabs WHERE studs = 'ИТ/О ИТ-15-2023 НБ' ORDER BY day, time;'''
    cur.execute(sql1)
    for i in cur.fetchall():
        print(i)
    cur.execute('''DELETE FROM studs WHERE ctid NOT IN (SELECT max(ctid) FROM studs GROUP BY studs.*);''')

    return result


@app.route('/')
def group_list():
    cur.execute('''SELECT studs FROM studs ORDER BY studs;''')
    groups = []
    for row in cur:
        groups.append(row[0])
    return render_template('groups.html', groups=groups)


@app.route('/group/<inst>/<text>')
def sheets(inst, text):
    group = (inst + '/' + text, )
    sql1 = '''SELECT * FROM tabs WHERE studs = %s ORDER BY day, time;'''
    cur.execute(sql1, group)
    arr = []
    lec = []
    t = []
    course = []
    for row in cur:
        arr.append(row[4])
        lec.append(row[1])
        t.append(row[2])
        course.append(row[3])
    return render_template('sheets.html', arr=arr, lec=lec, t=t, course=course)


if __name__ == '__main__':
    app.run()
