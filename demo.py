import tushare as ts

ts.set_token('16ba4ee3c92672e24b634d3d4cbcf43ec51d99e1dd676580a7ed1479')

pro = ts.pro_api()
# df = pro.trade_cal(exchange='SSE', is_open='1',
#                             start_date='20200101',
#                             end_date='20200401')
df = ts.pro_bar(ts_code='003188.SZ',
                asset='FD',
                    freq='1min',
                    start_date='2020-01-07 09:00:00',
                    end_date='2020-01-08 17:00:00')


print(df.shape)
print(df)