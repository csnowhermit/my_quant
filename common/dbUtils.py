import re
import pymysql

conn = pymysql.connect(host='127.0.0.1',
                           port=3306,
                           user='root',
                           password='123456',
                           database='fund',
                           charset='utf8mb4')
cursor = conn.cursor()

'''
    判断表是否存在
    :param table_name 表名
    :return True，表存在；False，表不存在
'''
def table_exists(table_name):
    sql = "show tables;"
    cursor.execute(sql)
    tables = [cursor.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return True
    else:
        return False

'''
    保存基金基本信息到数据库
    :param fundinfo dict
'''
def saveFundinfo2db(fundinfo):
    # 基金基本信息入库
    sql = '''
              insert into fund_info(fund_fullname, fund_name, fund_code, fund_type, issue_date,
                  build_date_and_scale, asset_size, slice_size, fund_admin, fund_custodian,
                  fund_manager, share_out_bonus, managerment_rate, custody_rate, sales_service_rate,
                  max_subscription_rate, max_purchasing_rate, max_redemption_rate, performance_baseline, tracking_target) VALUES (
                  '%s', '%s', '%s', '%s', '%s',
                  '%s', '%s', '%s', '%s', '%s',
                  '%s', '%s', '%s', '%s', '%s',
                  '%s', '%s', '%s', '%s', '%s')
          ''' % (
                 fundinfo['基金全称'], fundinfo['基金简称'], fundinfo['基金代码'], fundinfo['基金类型'], fundinfo['发行日期'],
                 fundinfo['成立日期/规模'], fundinfo['资产规模'], fundinfo['份额规模'], fundinfo['基金管理人'], fundinfo['基金托管人'],
                 fundinfo['基金经理人'], fundinfo['成立来分红'], fundinfo['管理费率'], fundinfo['托管费率'], fundinfo['销售服务费率'],
                 fundinfo['最高认购费率'], fundinfo['最高申购费率'], fundinfo['最高赎回费率'], fundinfo['业绩比较基准'], fundinfo['跟踪标的'])

    cursor.execute(sql)
    conn.commit()

