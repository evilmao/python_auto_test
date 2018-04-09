## XSTZ自动化测试框架
* 通过selenium+python实现主动监控  
* 全面转向UI自动化测试领域
## Description
* 自动化测试，定时测试，自动生成html报告，发送指定联系人，通过钉钉机器人实时播报，测试结果插入influxdb

## 环境

* windows 10/Linux/Mac os
* python 3.5+

## 依赖库

```shell
pip install -r requirements.txt
```

## Function

* 自动生成html报告

* 记录日志log

* sendemail

* 测试结果插入influxdb

  ​


## 运行方式

>  ```shell
>  cd XSTZ_Test_framework
>  python TestRunner.py
>  ```

## updata 

> auth: failymao 

> 1. Version 1.1  Date:1/3/2018
>
>    -  新增钉钉机器人自动播报；
>
>    * API，socket接口自动化测试（预留功能); 
>
>    * 优化Page类代码
>
>      ​
>
> 2. Version  1.2 Date: 8/3/2018
>
>    - 新增InfluxDB收集功能
>    - 重构Page-Object类
>    - "网页存款页面跳转"测试用例实现
>    - 钉钉机器人自动播报，消息播报格式重写
>    - 代码优化
>
> 3. version 1.3 Date: 23/3/2018
>
>    - Jenkins持续化集成测试
>    - 新增ddt驱动模块，根据测试通道自动匹配测试用例个数
>    - 页面类代码优化
> 4. version 1.4 Date 9/04/2018
>    - 集成Android端测试用例
> ​
>

## 目录结构说明

**src/utils 下的文件说明 **[^ *表示预留功能]

E:.src 
│   src_unitls.txt (目录文档说明)
│   
├───test  
│   │   
│   ├───case (所有测试类API,UI,SOCKET)  
│   │   │   
│   │   ├───API(API接口测试类文件)
│   │   │   │   test_xstz_http.py    
│   │   │   └───__init__.py
│   │   │           
│   │   ├───SOCKET(SOCKET接口测试)
│   │   │   │   test_socket.py  
│   │   │   └─── __init__.py
│   │   │           
│   │   ├───UI(UI自动化测试类)
│   │   │   │   test_login.py (核心测试代码)
│   │   │   │   test_login_bycookie.py (通过cookie登录，绕过验证码)
│   │   │   └───__init__.py
│   │   │           
│   │   └───__init__.py
│   │           
│   ├───common(封装的页面类文件)
│   │   │   browser.py (创建浏览器类，打开页面，关闭页面的操作)
│   │   │   page.py  (对打开页面后的一些基本操作类的封装，元素定位，等模拟人为的操作方法)
│   │   └─── __init__.py
│   │           
│   ├───mock (*预留功能--socket接口测试)
│   │   │   mock_socket_server.py  (服务端)  
│   │   └───__init__.py
│   │           
│   ├───page(PageObjects思想进一步封装，对每一个打开的页面进行相应的操作)
│   │   │   xstz_login_page.py (login页面类，公共类)
│   │   │   xstz_login_result_page.py (显示结果页面的操作) 
│   │   └───_init__.py
│   │           
│   ├───suite (测试套件，用来组织用例)
│   │ 	│   TestRunner.py(测试用例运行主程序)
│   │   └───__init__.py
│   │        
├───utils(测试支撑代码)
│   │   assertion.py  (*封装自己的断言，根据需要自己添加)
│   │   client.py	(*HTTP,TCP接口的封装)
│   │   config.py	(配置文件)
│   │   DingDingReport.py(顶顶机器人自动播报代码)
│   │   extractor.py	  (*封装抽取器，从结果抽取部分信息复用)
│   │   file_reader.py    (封装文件读取类,如读取yaml，excel等文件)
│   │   generator.py	  (*生成器封装)
│   │   HTMLTestRunner_Echarts.py (TestResult类封装,将测试结果生成html文件)
│   │   log.py					(log类的封装，用来定义自己的log)
│   │   SendEmail.py			(将测试报告通过Email发送给指定负责人)
│   │   support.py				(*支持方法，比如某些请求需要加密，数字验证)
│   │   Insert_InfluxDB.py		(对测试结果插入influxDB数据库)
│   └─── __init__.py
│           
└───__init__.py













[^ *表示预留功能]: 
