#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/8 10:22
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    : 
# @File    : run.py
# @Software: PyCharm
from src.config import BaseConfig, log_cost_time
from src.models.crfpp.bio_crf import CrfModel
from src.config import get_BaseConfig
print(1)
def run(s1 = 20):
    config = get_BaseConfig()
    config.logger.info('error')
    aim_str = r'研究证实，细胞减少与肺内病变程度及肺内炎性病变吸收程度密切相关。'
    aim_str = r'对儿童SARST细胞亚群的研究表明，与成人SARS相比，儿童细胞下降不明显，证明上述推测成立。'
    crf = CrfModel()
    # 将模型和特征工程需要的词典导入
    crf.load()



    res = crf.predict(aim_str)
    print(res)



run()
