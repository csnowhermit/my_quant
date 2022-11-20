import requests
import json
import re

'''
    获取天天基金实时数据，此接口只返回当天的数据，如遇非工作日，则返回前一天的数据
'''

'''
    获取指定基金的实时数据
    接口返回值：{fundcode: 基金代码, 
                name: 基金名称, 
                jzrq: 上一个交易日, 
                dwjz: 基金净值（截止上一交易日）, 
                gsz: 估算净值（实时）, 
                gszzl: 估算涨幅（实时）, 
                gztime: 更新时间（实时）}
'''
def get_fund_data_realtime(code):
    url = "http://fundgz.1234567.com.cn/js/%s.js" % code

    # 浏览器头
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    r = requests.get(url, headers=headers)
    # 返回信息
    content = r.text
    # content = """jsonpgz({"fundcode":"501019","name":"国泰国证航天军工指数","jzrq":"2020-08-13","dwjz":"1.2327","gsz":"1.2690","gszzl":"2.95","gztime":"2020-08-14 15:00"});"""

    # 正则表达式
    pattern = r'^jsonpgz\((.*)\)'
    # 查找结果
    search = re.findall(pattern, content)
    # 遍历结果
    for i in search:
        data = json.loads(i)
        print(type(data), data)
        print("基金: {}, 估算净值（实时）: {}".format(data['name'], data['gsz']))

if __name__ == '__main__':
    code = "003188"  # 基金代码
    get_fund_data_realtime(code)