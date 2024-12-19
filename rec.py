import time

from flask import Flask
import requests
import psycopg2 as ps
from bs4 import BeautifulSoup

app = Flask(__name__)
response = []
for i in range(2000, 4000, +1):
    print(i)
    try:
        rs = (requests.get('https://student.psu.ru/pls/stu_cus_et/tt_pkg.show_prep?P_TERM=&P_PEO_ID=&P_SDIV_ID='+str(i)+'&P_TY_ID=2024&P_WDAY=&P_WEEK=16', timeout=6))
        response.append(rs)
    except requests.exceptions.ConnectTimeout:
        print('FUCKINGTIMEOUT')
        i+=-1
        time.sleep(5)
@app.route('/<num>')
def hello_world(num):  # put application's code here
    num = int(num)
    result = response[0].text
    for i in range(0, 2000, +1):
        if response[i].text.find('8:00') != -1:
            print(i)
            result += response[i].text
    return result


if __name__ == '__main__':
    app.run()
