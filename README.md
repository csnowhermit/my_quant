# my_quant

# 1、数据接口

（1）所有基金名称列表：http://fund.eastmoney.com/js/fundcode_search.js

（2）所有基金公司名称列表代码：http://fund.eastmoney.com/js/jjjz_gs.js?dt=1463791574015

（3）获取指定基金的历史数据：

``` python
python tiantianjijin_onecode_history.py
```

​	结果保存在./data/fund_details_{code}.csv文件中。

（4）获取天天基金实时数据：http://fundgz.1234567.com.cn/js/{code}.js

``` python
python tiantianjijin_onecode_realtime.py
```

