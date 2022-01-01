# -*- coding: utf-8 -*-
"""
Author: shifulin
Email: shifulin666@qq.com
"""
import time
import requests
from md import MD

URL = "http://optiontools.cn/option_info/{spot}"
HEADER = ['code', 'year', 'month', 'expiry_date', 'remainder_days', 'underlying', 'strike_price', 'option_type']
CTP_MD_API = MD('future')


def get_option_info(spot):
    if spot == '000300':
        spot = 'IO'
    data = requests.get(URL.format(spot=spot)).json()
    print("数据更新日期:", data['date'])
    option_info_list = []
    for i in data['data']:
        assert len(i) == len(HEADER)
        item = dict(zip(HEADER, i))
        option_info_list.append(item)
        print(item)
    return option_info_list


def get_all_last_price():
    result = {}
    for k, v in CTP_MD_API.index.items():
        last_price = v.LastPrice
        # bid_price1 = v.BidPrice1
        # ask_price1 = v.AskPrice1
        result[k] = last_price
    return result


def main():
    if CTP_MD_API.login("tcp://180.166.0.226:31413",
                        "tcp://180.166.0.229:21413",
                        "tcp://140.206.102.130:31413",
                        15000):
        spot = 'cu'
        option_info_list = get_option_info(spot)
        code_set = set()
        for i in option_info_list:
            code_set.add(i['code'])
            code_set.add(i['underlying'])
        # print(code_set)
        CTP_MD_API.subscribe(list(code_set))
        while True:
            time.sleep(5)
            print(CTP_MD_API.is_connected())
            print(get_all_last_price())
    else:
        print("登陆失败", CTP_MD_API.is_connected())


if __name__ == '__main__':
    main()
