# -- coding utf-8 --
# @Time     2022/10/2 19:11
# @Author   dicardo
# @File     get_lottery.py
# @Software PyCharm

import bs4
import requests


def get_latest_number_by_500():
    url_500 = 'http://datachart.500.com/dlt/history/history.shtml'
    response_500 = requests.get(url_500)
    if not response_500.status_code == 200:
        return False
    soup_500 = bs4.BeautifulSoup(response_500.text, "html.parser")
    body_500 = soup_500.find('tbody', id="tdata")
    lottery_tr = body_500.find_all('tr')
    lottery_td = lottery_tr[0].find_all('td')
    return {
        'drawNum': lottery_td[0].text,
        'frontNum1': lottery_td[1].text,
        'frontNum2': lottery_td[2].text,
        'frontNum3': lottery_td[3].text,
        'frontNum4': lottery_td[4].text,
        'frontNum5': lottery_td[5].text,
        'backNum1': lottery_td[6].text,
        'backNum2': lottery_td[7].text,
        'drawTime': lottery_td[14].text,
    }
