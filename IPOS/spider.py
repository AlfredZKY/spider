import tushare as ts
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

ts.set_token('404ba015bd44c01cf09c8183dcd89bb9b25749057ff72b5f8671b9e6')
pro = ts.pro_api()

def get_code():
    # 获取所有的股票列表
    data = ts.get_stock_basics()

    # print(data.head())
    # Index(['name', 'industry', 'area', 'pe', 'outstanding', 'totals',
    #        'totalAssets', 'liquidAssets', 'fixedAssets', 'reserved',
    #        'reservedPerShare', 'esp', 'bvps', 'pb', 'timeToMarket', 'undp',
    #        'perundp', 'rev', 'profit', 'gpr', 'npr', 'holders'],
    #       dtype='object')
    # print(data.columns)

    # 获取环保类
    data = data[data.industry == '环境保护']
    # print(data.head())
    # print('环保股股票数量为:',len(data.industry))
    # 可以看到，环境保护股一共有66只，下面我们将用这66只股票的代码和名称，
    # 输入到pro.daily_basic()接口中，获取每只股票的每日数据，其中包括每日市值。
    # 时间期限从2009年1月1日至2019年11月10日，共11年的逐日数据。

    # pro = ts.pro_api()
    # ts_code='股票代码。格式为000002.SZ,可以为一只股票，也可以是列表组成的多支股票',
    # trade_date='',start_date='',end_date='' 三个为交易日期，也可以是固定日期
    # pro.daily_basic(ts_code='',trade_date='',start_date='',end_date='')
    data['code2'] = data.index

    # apply方法添加后缀
    data['code2'] = data['code2'].apply(lambda i:i+'.SZ')
    data = data.set_index(['code2'])
    # 将code和name转为dict,因为我们只需要表格中的代码和名称列
    data = data['name']
    data = data.to_dict()
    return data

def stock(key,start,end,value):
    # 添加代码列和名称列
    data = pro.daily_basic(ts_code=key,start_date=start,end_date=end)
    print(data)
    # 替换掉code后缀.SZ,regex设置为True才行
    # data['code'] = data['ts_code'].replace('.SZ','',regex=True)

def main():
    ts_code = get_code()
    start = '20090101'
    end = '20191110'
    keys = list(ts_code.keys())
    values = list(ts_code.values())

    for key,value in ts_code.items():
        stock(key,start,end,value)



if __name__ == '__main__':
    main()





