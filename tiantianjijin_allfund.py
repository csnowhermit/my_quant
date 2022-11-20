import re
import json
import requests

'''
    获取天天基金网所有基金列表
    数据接口：
    1.所有基金名称列表代码：http://fund.eastmoney.com/js/fundcode_search.js
    2.所有基金公司名称列表代码：http://fund.eastmoney.com/js/jjjz_gs.js?dt=1463791574015
'''

def get_all_fund_code():
    url = "http://fund.eastmoney.com/js/fundcode_search.js"

    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    response = requests.get(url, headers=headers)
    content = response.text
    content = content.replace("var r = ", "")
    content = content[0: -1]
    content = content.replace("[", "").replace("]", "").replace('"', '')
    # print(content)

    arr = content.split(",")
    code_list = []
    for i in range(0, len(arr), 5):
        code_list.append(arr[i])
    return code_list


if __name__ == '__main__':
    code_list = get_all_fund_code()
    print(len(code_list))
    print(code_list)
