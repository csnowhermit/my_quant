import time
import random
import requests
import pymysql
from bs4 import BeautifulSoup
from tqdm import tqdm

from common.dbUtils import saveFundinfo2db
from tiantianjijin_allfund import get_all_fund_code

'''
    获取指定基金的基本信息
'''

# 获取基金基本信息
def query_fund_basic(code):
    # http://fundf10.eastmoney.com/jbgk_005585.html
    response = requests.get("http://fundf10.eastmoney.com/jbgk_{}.html".format(code))
    resp_body = response.text
    soup = BeautifulSoup(resp_body, 'lxml')
    body_list = soup.find_all("table")
    basic_info = body_list[1]
    # print(basic_info)
    tr_list = basic_info.find_all("td")

    # 基金的基础信息
    result_dict = {}
    result_dict['基金全称'] = tr_list[0].get_text()
    result_dict['基金简称'] = tr_list[1].get_text()
    result_dict['基金代码'] = tr_list[2].get_text()
    result_dict['基金类型'] = tr_list[3].get_text()
    result_dict['发行日期'] = tr_list[4].get_text()
    result_dict['成立日期/规模'] = tr_list[5].get_text()
    result_dict['资产规模'] = tr_list[6].get_text()
    result_dict['份额规模'] = tr_list[7].get_text()
    result_dict['基金管理人'] = tr_list[8].get_text()
    result_dict['基金托管人'] = tr_list[9].get_text()
    result_dict['基金经理人'] = tr_list[10].get_text()
    result_dict['成立来分红'] = tr_list[11].get_text()
    result_dict['管理费率'] = tr_list[12].get_text()
    result_dict['托管费率'] = tr_list[13].get_text()
    result_dict['销售服务费率'] = tr_list[14].get_text()
    result_dict['最高认购费率'] = tr_list[15].get_text()
    result_dict['最高申购费率'] = tr_list[16].get_text()
    result_dict['最高赎回费率'] = tr_list[17].get_text()
    result_dict['业绩比较基准'] = tr_list[18].get_text()
    result_dict['跟踪标的'] = tr_list[19].get_text()

    return result_dict


if __name__ == '__main__':
    code_list = ['003188', '005918', '180012', '090013', '320010', '002001']
    # code_list = get_all_fund_code()

    # 逐个获取详细信息
    for code in tqdm(code_list):
        result_dict = query_fund_basic(code)
        print(result_dict)
        saveFundinfo2db(result_dict)

        time.sleep(random.uniform(0, 2))



