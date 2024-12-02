# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :binance_rank.py
# @Time      :2024/12/2 10:55
# @Author    :MA1688
# @Software  :PyCharm

import time

import httpx
import pandas as pd
from tabulate import tabulate

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class BinanceRank:
    """
    币安全部币种每日交易排名
    """

    def __init__(self):
        self.url = "https://fapi.binance.com/fapi/v1/ticker/24hr"

    def get_rank_data(self, symbol=None):
        """
        获取合约币种交易涨幅数据
        :param symbol: 币种
        :return:
        """
        try:

            resp = httpx.get(url=self.url, params={"symbol": symbol})
            print(f"目前已使用权重: {resp.headers['X-MBX-USED-WEIGHT-1M']}")
            resp = resp.json()
            return resp

        except Exception as e:
            print(f"获取币种排名失败: {e}")

    def get_rank(self, symbol_data):
        """
        获取币种排名
        :param symbol_data: 币种
        :return:
        """

        # 筛选币对类型
        symbol_data = [data for data in symbol_data if data['symbol'].endswith('USDT')]

        pd_data = pd.DataFrame(symbol_data)  # 转换为 DataFrame

        # 将 'priceChangePercent' 列转换为数值类型
        pd_data['priceChangePercent'] = pd.to_numeric(pd_data['priceChangePercent'], errors='coerce')

        # 使用 nlargest 方法获取价格变动百分比最大的前十名
        top_price_changes = pd_data.nlargest(10, 'priceChangePercent').reset_index(drop=True)
        # 使用 nsmallest 方法获取价格变动百分比最小的前十名
        bottom_price_changes = pd_data.nsmallest(10, 'priceChangePercent').reset_index(drop=True)

        print("Top 10 Price Changes:")

        custom_headers = ['symbol', '价格变动', '格变动百分比', '加权平均价', '最近一次成交价', '最近一次成交额',
                          '第一次成交的价格', '最高价', '最低价',
                          '成交量', '成交额', '第一笔交易的发生时间', '最后一笔交易的发生时间', '首笔成交id',
                          '末笔成交id', '成交笔数']
        print(tabulate(top_price_changes, headers=custom_headers, tablefmt='pretty'))
        print()


if __name__ == '__main__':
    binance = BinanceRank()
    symbols = None
    while True:
        resp_data = binance.get_rank_data(symbols)
        binance.get_rank(resp_data)
        time.sleep(0.168)
