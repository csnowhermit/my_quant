import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


'''
    获取基金数据
    数据来源：和讯网
'''

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
)
dcap["phantomjs.page.settings.resourceTimeout"] = 1000
dcap["phantomjs.page.settings.loadImages"] = False  # 不加载图片，加快速度
dcap["phantomjs.page.settings.disk-cache"] = True  # 启用缓存
dcap["phantomjs.page.settings.userAgent"] = "faking it"
dcap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = False
dcap["phantomjs.page.settings.ignore-ssl-errors"] = True

driver = webdriver.PhantomJS(executable_path='D:/opt/phantomjs-2.1.1-windows/bin/phantomjs.exe',
                             desired_capabilities=dcap)

# 获取网页数据
def getSoup(url):
    driver.get(url)
    content = driver.page_source  # 获取网页内容
    soup = BeautifulSoup(content, 'xml')
    return soup
    # getInfo(soup)

# 存入csv文件
def saveCsv(soup):
    # fld_enddate 日期，fld_unitnetvalue 单位净值，fld_netvalue 累计净值
    dateList = []
    unitnetvalueList = []
    netvalueList = []
    for x in soup.find_all('Data'):
        dateList.append(str(x.find_all('fld_enddate')[0].contents[0]))
        unitnetvalueList.append(float(x.find_all('fld_unitnetvalue')[0].contents[0]))
        netvalueList.append(float(x.find_all('fld_netvalue')[0].contents[0]))
    fundData = pd.DataFrame()
    fundData['sdate'] = dateList
    fundData['unitnetvalue'] = unitnetvalueList
    fundData['netvalue'] = netvalueList
    # print(fundData.head())
    fundData.to_csv(code + '.csv', mode='w')
    print('%s saved to csv' % code)
    return fundData


if __name__ == '__main__':
    # 基金代码
    codes = ['110022', '180012', '090013', '320010', '002001', '003188']
    for code in codes:
        # url = "http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?" \
        #     "fundcode=" + code + "&startdate=2018-01-01&enddate=2018-03-31"
        url = "http://data.funds.hexun.com/outxml/detail/openfundnetvalue.aspx?fundcode=" + code
        soup = getSoup(url)
        fund_data = saveCsv(soup)