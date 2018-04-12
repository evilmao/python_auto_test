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



![](http://ww1.sinaimg.cn/large/8599e4cfly1fqa28qczyaj20ta0swtbe.jpg)





[^ *表示预留功能]: 
