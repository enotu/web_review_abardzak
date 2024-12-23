import time

from flask import Flask
import requests, re
import psycopg2 as ps
from bs4 import BeautifulSoup


app = Flask(__name__)
response = []
try:
    rs = (requests.get('https://student.psu.ru/pls/stu_cus_et/tt_pkg.show_prep?P_TERM=&P_PEO_ID=&P_SDIV_ID=&P_TY_ID=2024&P_WDAY=&P_WEEK=17', timeout=30))
    response.append(rs)
except requests.exceptions.ConnectTimeout:
    print('FUCKINGTIMEOUT')
    time.sleep(15)

r_lec = [r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>старший преподаватель)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))', r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>преподаватель)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))', r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>Док.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))', r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>Кан.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))', r'^(?P<Name>.*?\s+.*?\s+.*?)(?P<judge>ассистент.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))']
r_left = r"(?P<Name>.*?\s+.*?\s+.*?)\s+(?P<Date>\d{1}\.\d{1}\.\d{1})\s+(?P<end>\(.*?\))"
@app.route('/<num>')
def hello_world(num):
    result = response[0].text
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
                        continue
                    if item[2] != ':' and item[1] != ':':
                        if re.match(r_left, item) is not None:
                            lector = item
                            for reg in r_lec:
                                try:
                                    if re.match(reg, lector) is not None:
                                        lc=re.split(reg, lector)
                                    else:
                                        continue
                                    lector = lc[1]
                                except:
                                    continue
                        else:
                            tblrs = item.split('\n')
                            for tblr in tblrs:
                                if re.match(r'[А-ЯёЁ]{2}/[А-ЯёЁ]\s[А-ЯёЁ]{3}-\d-20\d\d\s[А-ЯёЁ]{2}', tblr) is not None:
                                    print(tblr)
                    else:
                        time_start = item
                    continue


    return result


if __name__ == '__main__':
    app.run()
