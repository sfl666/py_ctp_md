# -*- coding: utf-8 -*-
"""
Author: shifulin
Email: shifulin666@qq.com
"""
import os
from ctypes import CDLL, POINTER, create_string_buffer, cast, byref
from ctypes import Structure, c_char_p, c_void_p, c_char, c_int, c_double, c_bool, c_ulong


class DepthMarketData(Structure):
    _fields_ = [
        ('TradingDay', c_char * 9),  # 交易日
        ('InstrumentID', c_char * 31),  # 合约代码
        ('ExchangeID', c_char * 9),  # 交易所代码
        ('ExchangeInstID', c_char * 31),  # 合约在交易所的代码
        ('LastPrice', c_double),  # 最新价
        ('PreSettlementPrice', c_double),  # 上次结算价
        ('PreClosePrice', c_double),  # 昨收盘
        ('PreOpenInterest', c_double),  # 昨持仓量
        ('OpenPrice', c_double),  # 今开盘
        ('HighestPrice', c_double),  # 最高价
        ('LowestPrice', c_double),  # 最低价
        ('Volume', c_int),  # 数量
        ('Turnover', c_double),  # 成交金额
        ('OpenInterest', c_double),  # 持仓量
        ('ClosePrice', c_double),  # 今收盘
        ('SettlementPrice', c_double),  # 本次结算价
        ('UpperLimitPrice', c_double),  # 涨停板价
        ('LowerLimitPrice', c_double),  # 跌停板价
        ('PreDelta', c_double),  # 昨虚实度
        ('CurrDelta', c_double),  # 今虚实度
        ('UpdateTime', c_char * 9),  # 最后修改时间
        ('UpdateMillisec', c_int),  # 最后修改毫秒
        ('BidPrice1', c_double),  # 申买价一
        ('BidVolume1', c_int),  # 申买量一
        ('AskPrice1', c_double),  # 申卖价一
        ('AskVolume1', c_int),  # 申卖量一
        ('BidPrice2', c_double),  # 申买价二
        ('BidVolume2', c_int),  # 申买量二
        ('AskPrice2', c_double),  # 申卖价二
        ('AskVolume2', c_int),  # 申卖量二
        ('BidPrice3', c_double),  # 申买价三
        ('BidVolume3', c_int),  # 申买量三
        ('AskPrice3', c_double),  # 申卖价三
        ('AskVolume3', c_int),  # 申卖量三
        ('BidPrice4', c_double),  # 申买价四
        ('BidVolume4', c_int),  # 申买量四
        ('AskPrice4', c_double),  # 申卖价四
        ('AskVolume4', c_int),  # 申卖量四
        ('BidPrice5', c_double),  # 申买价五
        ('BidVolume5', c_int),  # 申买量五
        ('AskPrice5', c_double),  # 申卖价五
        ('AskVolume5', c_int),  # 申卖量五
        ('AveragePrice', c_double),  # 当日均价
        ('ActionDay', c_char * 9),  # 业务日期
    ]


class MD(object):

    def __init__(self, label):
        self.index = {}

        self.dll = CDLL(os.path.join(os.path.dirname(os.path.abspath(__file__)), f'{label}.dll'))

        char_array_p = POINTER((c_char * 31))
        self._subscribe = self.dll.subscribe
        self._subscribe.argtypes = [char_array_p, c_int]

        self._unsubscribe = self.dll.unsubscribe
        self._unsubscribe.argtypes = [char_array_p, c_int]

        self._get_tick_data = self.dll.get_tick_data
        self._get_tick_data.argtypes = [c_char_p]
        self._get_tick_data.restype = c_void_p

        self._is_api_ok = self.dll.is_api_ok
        self._is_api_ok.argtypes = []
        self._is_api_ok.restype = c_bool

        self._is_connected = self.dll.is_connected
        self._is_connected.argtypes = []
        self._is_connected.restype = c_bool

        self._login = self.dll.login
        self._login.argtypes = [c_char_p, c_char_p, c_char_p, c_ulong]
        self._login.restype = c_int

    def login(self, front_addr1, front_addr2, front_addr3, timeout_ms):
        return self._login(c_char_p(front_addr1.encode()), c_char_p(front_addr2.encode()),
                           c_char_p(front_addr3.encode()), timeout_ms) == 1

    def is_ok(self):
        return self._is_api_ok()

    def is_connected(self):
        return self._is_connected()

    def subscribe(self, instrument_list):
        length = len(instrument_list)
        instrument_array = ((c_char * 31) * length)()
        for index, instrument in enumerate(instrument_list):
            instrument_array[index] = create_string_buffer(instrument.encode(), 31)
        self._subscribe(byref(instrument_array[0]), length)
        for instrument in instrument_list:
            if instrument not in self.index:
                tick_data = self._get_tick_data(c_char_p(instrument.encode()))
                self.index[instrument] = cast(tick_data, POINTER(DepthMarketData))[0]

    def unsubscribe(self, instrument_list):
        length = len(instrument_list)
        instrument_array = ((c_char * 31) * length)()
        for index, instrument in enumerate(instrument_list):
            instrument_array[index] = create_string_buffer(instrument.encode(), 31)
        self._unsubscribe(byref(instrument_array[0]), length)
        for instrument in instrument_list:
            if instrument in self.index:
                del self.index[instrument]

    def tick(self, instrument):
        return self.index[instrument]

