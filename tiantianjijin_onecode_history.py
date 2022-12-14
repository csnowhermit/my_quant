import re
import time
import random
import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import matplotlib

'''
    指定code抓取指定时间段的所有数据：历史数据
    数据来源：天天基金网
'''

#指定默认字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['font.family']='sans-serif'
#解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False

'''
    请求网页
'''
def get_url(url, params=None, proxies=None):
    rsp = requests.get(url, params=params, proxies=proxies)
    rsp.raise_for_status()
    return rsp.text

'''
    从网页抓取基金数据
    :code 基金代码
    :per 每页显示多少条数据
    :param start_date 抓取数据的起始日期
    :param end_date 抓取数据的终止日期，和起始日期缺失则抓取全部日期的
    :return records 直接返回爬取的list
'''
def get_fund_data(code, per=10, start_date='', end_date='', proxies=None):
    url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx'
    params = {'type': 'lsjz', 'code': code, 'page':1,'per': per, 'sdate': start_date, 'edate': end_date}
    html = get_url(url, params, proxies)
    soup = BeautifulSoup(html, 'html.parser')

    # 获取总页数
    pattern=re.compile(r'pages:(.*),')
    result=re.search(pattern,html).group(1)
    pages=int(result)

    # 获取表头
    heads = []
    for head in soup.findAll("th"):
        heads.append(head.contents[0])

    # 数据存取列表
    records = []

    # 从第1页开始抓取所有页面数据
    page=1
    while page<=pages:
        params = {'type': 'lsjz', 'code': code, 'page':page,'per': per, 'sdate': start_date, 'edate': end_date}
        html = get_url(url, params, proxies)
        soup = BeautifulSoup(html, 'html.parser')

        # 获取数据
        for row in soup.findAll("tbody")[0].findAll("tr"):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents

                # 处理空值
                if val == []:
                    row_records.append(np.nan)
                else:
                    row_records.append(val[0])

            # 记录数据
            records.append(row_records)
        # 下一页
        page=page+1

    # 数据整理到dataframe
    np_records = np.array(records)
    data= pd.DataFrame()
    for col,col_name in enumerate(heads):
        data[col_name] = np_records[:,col]
    return data


if __name__ == "__main__":
    code_list = ['003188', '005918', '180012', '090013', '320010', '002001']
    for code in tqdm(code_list):
        data = get_fund_data(code, per=10)    # 不加起止日期表示获取基金的全部数据 , sdate='2018-01-01', edate='2022-11-19'

        # 修改数据类型
        data['净值日期'] = pd.to_datetime(data['净值日期'],format='%Y/%m/%d')
        data['单位净值'] = data['单位净值'].astype(float)
        data['累计净值'] = data['累计净值'].astype(float)
        data['日增长率'] = data['日增长率'].str.strip('%').astype(float)

        # 按照日期升序排序并重建索引
        data = data.sort_values(by='净值日期', axis=0, ascending=True).reset_index(drop=True)
        print(code, data.shape)
        # print(data)

        data.to_csv('./data/fund_details_%s.csv' % code, header=True)
        time.sleep(random.uniform(0, 2))

    # # 获取净值日期、单位净值、累计净值、日增长率等数据并
    # net_value_date = data['净值日期']
    # net_asset_value = data['单位净值']
    # accumulative_net_value=data['累计净值']
    # daily_growth_rate = data['日增长率']
    #
    # # 作基金净值图
    # fig = plt.figure()
    # #坐标轴1
    # ax1 = fig.add_subplot(111)
    # ax1.plot(net_value_date,net_asset_value)
    # ax1.plot(net_value_date,accumulative_net_value)
    # ax1.set_ylabel('净值数据')
    # ax1.set_xlabel('日期')
    # plt.legend(loc='upper left')
    # #坐标轴2
    # ax2 = ax1.twinx()
    # ax2.plot(net_value_date,daily_growth_rate,'r')
    # ax2.set_ylabel('日增长率（%）')
    # plt.legend(loc='upper right')
    # plt.title('基金净值数据')
    # plt.show()
    #
    # # 绘制分红配送信息图
    # bonus = accumulative_net_value-net_asset_value
    # plt.figure()
    # plt.plot(net_value_date,bonus)
    # plt.xlabel('日期')
    # plt.ylabel('累计净值-单位净值')
    # plt.title('基金“分红”信息')
    # plt.show()
    #
    # # 日增长率分析
    # print('日增长率缺失：',sum(np.isnan(daily_growth_rate)))
    # print('日增长率为正的天数：',sum(daily_growth_rate>0))
    # print('日增长率为负（包含0）的天数：',sum(daily_growth_rate<=0))