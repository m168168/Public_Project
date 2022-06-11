#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/4 9:49
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    : 
# @File    : config.py
# @Software: PyCharm
import configparser
import os
import time
from src.utils.tools import BaseConfig,get_parent_dir

# 获取当前路径
current_path = get_parent_dir()      # os.path.abspath(os.curdir)  current_path = os.path.abspath('.')
# 项目路径
project_path = get_parent_dir(current_path,-2)
# config.ini 配置路径
config_path = os.path.join(project_path,'config.ini')
# 当没有给日志保存路径，即创建下面路径
logdir_path = os.path.join(project_path,'logs')



def get_BaseConfig():
    """
    基本的配置初始化
    :return:
    """
    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    if len(config.get('logs', 'logdir_path')) == 0:
        print("***没有初始化日志保存路径，已经自动添加到项目路径:\t%s" % logdir_path)
        config.set('logs', 'logdir_path', logdir_path)
    base_confg = BaseConfig(project_path=project_path,config=config)
    return base_confg

baseConfig= get_BaseConfig()
# 记录每个程序所用时间的装饰器
def log_cost_time(func):
    def wrapper(*args, ** kwargs):
        # todo before fun ()
        start_time = time.time()
        result = func(*args,**kwargs)
        time_cost_ms = time.time() - start_time
        baseConfig.logger.info('func: '+str(func.__name__)+' cost Time:'+str(time_cost_ms))
        # todo atger fun()
        return result
    return wrapper
