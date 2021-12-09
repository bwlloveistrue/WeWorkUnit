# -*- coding: utf-8 -*-
# Author: bwl
# Create Date: 2020.12.06
import os
import logging

class My_Logger(object):
    """
    自定义日志类。日志分两类：
        1.总体日志，记录日志执行整体过程，存放在./log目录下，命名读取配置文件logFileName参数
        2.测试日志，记录测试执行过程中的详细日志。有两部分：
            （1）debug log，记录从浏览器打开到结束所有的详细过程，按./log/starttime//browser/runtime/testname记录
            （2）error log，只记录错误日志，日志将被记录在html结果文件中
    """
    def __init__(self, logger_name='Auto Test'):
        self.logger = logging.getLogger(logger_name)
        # 日志输出格式
        self.formatter = logging.Formatter("%(asctime)s - %(levelname)-4s - %(message)s")
        # 指定日志的最低输出级别，默认为WARN级别
        self.logger.setLevel(logging.INFO)

    def get_handler(self, file_path):
        # 生成文件日志的handler
        p, f = os.path.split(file_path)
        if not (os.path.exists(p)):
            os.makedirs(p)  # 判断是否存在该路径，如果不存在就新创建
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(self.formatter)
        return file_handler