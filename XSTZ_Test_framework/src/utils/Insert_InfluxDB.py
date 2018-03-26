# -*- coding:utf-8 -*-
# author by Failymao

"""
- 测试结果插入到influxDB数据库
"""
from influxdb import InfluxDBClient
from src.utils.config import Config
from src.utils.log import logger

conn_dict = Config().get("conn_dict")


def insert_influxdb(test_data):
    try:
        client = InfluxDBClient(**conn_dict)
        logger.info("Connect influxdb server successfully!")
    except Exception as e:
        logger.error("Connect influxdb failed !Reason:{}".format(e))

    if test_data:
        for test_action, data in test_data["suite"].items():
            influxdb_data = [
                {"measurement": "XSTZ_WAP_TEST",
                 "tags": {
                     "IsSuccess": data["IsSuccess"],
                     "test_action":test_action
                 },
                 "fields":{"ReturnCode": data["ReturnCode"]}
                 }
            ]
            try:
                client.write_points(influxdb_data)
                logger.info("success to insert data to influxDB!")
            except Exception as e:
                logger.error(
                    "Insert to InfluxDB fail, check the reason! {}".format(e))


if __name__ == "__main__":
    print(conn_dict)
