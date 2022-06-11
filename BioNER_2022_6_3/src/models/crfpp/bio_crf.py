#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/5 17:23
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    : 
# @File    : bio_crf.py
# @Software: PyCharm

import os
import sys
import CRFPP
import jieba

from src.config import log_cost_time

abs_path = os.path.abspath(__file__)
cur_path = os.path.abspath(f"{abs_path}/..")
sys.path.insert(0, cur_path)
model_path = "model.2022.6.6"
CRF_MODEL_PATH = os.path.join(cur_path, model_path)

name_list=r'对儿童SARST细胞亚群的研究表明，与成人SARS相比，儿童细胞下降不明显，证明上述推测成立。'

class FeatureEngineer():
    def __init__(self,aim_str:str):
        self.aim_str = aim_str #句子要做的特征工程
        self.insert_fe = []  # 总共要做的特征工程
        self.input = [] # 经过特征工程后，输入crf++模型的进行预测
    def add_feature(self):
        """
        特征工程 ： 根据实际情况做符合的特征
        其中要和训练的时候，保持特征工程一致
        :return:
        """
        # todo  构建医疗词库 ，  如果 某个词属于这个词库 就将它置为1 else 0
        #加入结巴分词特征
        self.cut_str = list(jieba.cut(self.aim_str))
        BIOES = []
        for j in range(len(self.cut_str)):
            if len(self.cut_str[j]) == 1:
                if self.cut_str[j] == "与":
                    BIOES.append("O")
                else:
                    BIOES.append("S")
            else:
                for k in range(len(self.cut_str[j])):
                    if k == 0:
                        BIOES.append("B")
                    elif k == len(self.cut_str[j]) - 1:
                        BIOES.append("E")
                    else:
                        BIOES.append("I")
        self.insert_fe.append(BIOES)


        return self.insert_fe

    def format_input(self):
        """
        将特征 和原始文本拼接成CRF++ 能测试的模板
        :return:
        """
        # self.add_feature()  # 特征工程
        for i in range(len(self.aim_str)):
            x = ""
            x += self.aim_str[i]
            x += "\t"
            for j in range(len(self.insert_fe)):
                x += str(self.insert_fe[j][i])
                x += "\t"
            self.input.append(x[:-1])
        return  self.input

class CrfModel():
    def __init__(self,model_path=CRF_MODEL_PATH):
        self.model_path = model_path
        self.aim_str = ""
        self.input = []
        self.res = {}
    def load(self):
        self.tagger = CRFPP.Tagger("-m %s -v 2" % self.model_path)

    def featureEngineering(self):
        self.input = FeatureEngineer(self.aim_str).format_input()

    @log_cost_time
    def predict(self,aim_str):
        self.aim_str = aim_str
        self.featureEngineering()
        self.tagger.clear()
        for word in self.input:
            self.tagger.add("{}".format(word))
        self.tagger.parse()
        size = self.tagger.size()
        self.predict_tags = [self.tagger.y2(i) for i in range(0, size)]
        self.res["confidence"] = self.tagger.prob()
        self.format_res()
        return self.res

    def format_res(self):
        data = []
        tmp = ["", ""]
        for i in range(len(self.aim_str)):
            sign = self.predict_tags[i][0]
            if sign in ["O"]:
                tmp[0] = self.aim_str[i]
                tmp[1] = self.predict_tags[i]
                data.append((tmp[0], tmp[1]))
                tmp = ["", ""]
            elif sign in ["S"]:
                tmp[0] = name_list[i]
                tmp[1] = self.predict_tags[i][2:]
                data.append((tmp[0], tmp[1]))
                tmp = ["", ""]
            elif sign in ['E']:
                tmp[0] += name_list[i]
                tmp[1] = self.predict_tags[i][2:]
                data.append((tmp[0], tmp[1]))
                tmp = ["", ""]
            else:
                tmp[0] += self.aim_str[i]
        self.res["data"] = data

if __name__ == '__main__':
    aim_str = r'研究证实，细胞减少与肺内病变程度及肺内炎性病变吸收程度密切相关。'
    aim_str = r'对儿童SARST细胞亚群的研究表明，与成人SARS相比，儿童细胞下降不明显，证明上述推测成立。'
    crf = CrfModel()
    # 将模型和特征工程需要的词典导入
    crf.load()
    res = crf.predict(aim_str)
    print(res )