#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/4 18:16
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    : 
# @File    : tools.py
# @Software: PyCharm

import os
import time
import logging
import configparser
import logging.config
import threading
from logging.handlers import RotatingFileHandler

def get_parent_dir(path=None, offset=-1)->str:
    """
    返回某个路径的，offset 父路径
    :param path: 某个路径
    :param offset:  返回上一级的 个数
    :return:  父路径
    """
    result = path if path else __file__
    for i in range(abs(offset)):
        result = os.path.dirname(result)
    return result

def singleton(cls):
    """
    一个装饰器，来装饰我们需要指定的单例类
    :param cls:
    :return:
    """
    _instance = {}   # 创建一个字典用来保存被装饰类的实例对象
    def wapper(*args ,**kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args,**kwargs)
        return _instance[cls]
    return wapper

class Singleton(object):
    """
    定义一个单例模型类 其他单例类可以继承
    https://www.jb51.net/article/132436.htm
    """
    _instance_lock = threading.Lock()  # 加锁
    _init_flag = False  # 记录是否执行初始化动作,保证只初始化一次
    def __init__(self):
        if Singleton._init_flag :
            return
        Singleton._init_flag = True
    def __new__(cls ,*args ,**kwargs):
        if not hasattr(cls, "_instance"):
            with Singleton._instance_lock:
                if not hasattr(cls,'_instance'):
                    # cls._instance = object.__new__(cls)  # 调用父类创建
                    cls._instance = super(Singleton,cls).__new__(cls) # 调用父类创建
        return cls._instance


class Logs(Singleton):
    _init_flag = False  # 记录是否执行初始化动作
    def __init__(self,config):
        if Logs._init_flag:  # 保证创建的对象只初始化一次
            return
        Logs._init_flag = True
        self.config = config
        self.logdir_path = self.config.get('logs','logdir_path')
    def _logs_config(self ):
        """
          #创建日志功能 初始化配置
        :return:
        """
        try:
            # 定义三种日志输出格式 开始
            standard_format = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]' \
                              '[%(levelname)s][%(message)s]'  # 其中name为getLogger()指定的名字；lineno为调用日志输出函数的语句所在的代码行
            simple_format = '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]%(message)s'
            id_simple_format = '[%(levelname)s][%(asctime)s] %(message)s'
            logfile_default = self.config.get('logs','logfile_default') # 日志文件保存路径
            logfile_error = self.config.get('logs','logfile_error')
            if not os.path.exists(self.logdir_path): # 如果不存在定义的日志目录就重新创建一个
                os.mkdir(self.logdir_path)
            logfile_path = os.path.join(self.logdir_path,logfile_default ) # log文件的全路径
            logfile_error_path = os.path.join(self.logdir_path,logfile_error)
            LOGGING_DIC = {  # 日志文件的配置文件
                'version': 1,
                'disable_existing_loggers': False,
                'formatters': {
                    'standard': {
                        'format': standard_format
                    },
                    'simple': {
                        'format': simple_format
                    },
                },
                'filters': {},  # filter可以不定义
                'handlers': {
                    # 打印到终端的日志
                    'console': {
                        'level': 'DEBUG',
                        'class': 'logging.StreamHandler',  # 打印到屏幕
                        'formatter': 'simple'
                    },
                    # 打印到文件的日志,收集info及以上的日志
                    'default': {
                        'level': 'INFO',
                        'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件
                        'formatter': 'standard',
                        'filename':logfile_path ,  # 日志文件
                        'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M  (*****)
                        'backupCount': 5,
                        'encoding': 'utf-8',  # 日志文件的编码，再也不用担心中文log乱码了
                    },
                    # 打印到文件的日志:收集错误及以上的日志
                    'error': {
                        'level': 'ERROR',
                        'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
                        'filename': logfile_error_path,  # 日志文件
                        'maxBytes': 1024 * 1024 * 5,  # 日志大小 5M
                        'backupCount': 5,
                        'formatter': 'standard',
                        'encoding': 'utf-8',
                    },

                },
                'loggers': {
                    # logging.getLogger(__name__)拿到的logger配置。如果''设置为固定值logger1，则下次导入必须设置成logging.getLogger('logger1')
                    '': {
                        # 这里把上面定义的两个handler都加上，即log数据既写入文件又打印到屏幕
                        'handlers': ['default', 'console'],
                        'level': 'DEBUG',
                        'propagate': False,  # 向上（更高level的logger）传递
                    },
                },
            }
            return LOGGING_DIC
        except Exception as e :
            raise  Exception(str(e))

    # 创建日志
    def load_my_logging_cfg(self ):
        LOGGING_DIC = self._logs_config()
        logging.config.dictConfig(LOGGING_DIC)  # 导入上面定义的logging配置
        logger = logging.getLogger(__name__)  # 生成一个log实例
        # logger.info('It works!')  # 记录该文件的运行状态
        return logger

# 配置类 使用单例模式
class BaseConfig(Singleton):
    _init_flag = False  # 记录是否执行初始化动作
    def __init__(self,project_path, config):
        if BaseConfig._init_flag:  # 保证创建的对象只初始化一次
            return
        BaseConfig._init_flag = True
        # 类初始化
        self.project_path = project_path
        self.config = config
        self.data_dirs = self.config.get('datasets', 'data_dir')
        self.logger = Logs(self.config).load_my_logging_cfg()
    @property
    def loggers(self):
        return self.logger
    @property
    def configs(self):
        return self.config
    @property
    def data_dir(self):
        return self.data_dirs


