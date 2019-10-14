import pandas as pd 
import csv

## 爬取中商情报网上的上市公司
name = list(["序号","股票代码","股票简称","公司名称","省份","城市","主营业务收入(201712)","净利润(201712)","员工人数","上市日期","招股书","公司财报","行业分类","产品类型","主营业务"])
for i in range(1,4):
    url = 'http://s.askci.com/stock/a/?reportTime=2017-12-31&pageNum=%s' % str(i)
    tb = pd.read_html(url)[3] # 经观察发现所需表格是网页中第4个表格，故为[3]
    tb.to_csv(r'2.csv',mode='a',encoding='utf-8_sig',header=name,index=0)
    print('第' + str(i) + '页抓取完成')

print(pd.read_csv(r'2.csv').drop_duplicates())

