#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/5 18:16
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    : 
# @File    : process_data.py
# @Software: PyCharm

import os
from src.config import get_BaseConfig
baseconfig = get_BaseConfig()

class DataProcess():
    def __init__(self,data_dir= baseconfig.data_dir):
        """

        :param data_dir:
        """
        self.data_dir = data_dir
        self.train_path = os.path.join(self.data_dir, 'train.txt')
        self.test_path = os.path.join(self.data_dir, 'test.txt')
        self.dev_path = os.path.join(self.data_dir, 'validation.txt')
        self.train_format_path = os.path.join(self.data_dir, 'trainFormat.txt') # 转成训练格式文件
        self.dev_format_path = os.path.join(self.data_dir, 'validationFormat.txt')
        self.test_format_path = os.path.join(self.data_dir, 'testFormat.txt')

    def _transfor_BIOES(slef,sentence: str) -> {}:
        """
        将sentence -> BIOES
        :param sentence:
        :return:  {sen: , label: }
        """
        try:
            res = {}
            sen_label = []  # BIOES标注结果
            s_split = sentence.split('|||')
            num_tags = len(s_split)
            if num_tags > 0:
                sen = s_split[0]
                sen_len = len(sen)
                sen_label = ['O'] * sen_len
                for e in s_split[1:]:  # 对标注的每一个实体进行转换
                    e = e.split()
                    if len(e) == 3:
                        start = int(e[0])
                        end = int(e[1])
                        label = e[-1]
                        span = end - start
                        if span == 0:  # 单个实体实体标注
                            sen_label[start] = 'S-' + label
                        else:  # 连续实体标注
                            sen_label[start] = r'B-' + label
                            sen_label[end] = r'E-' + label
                            if span > 1:
                                sen_label[start + 1:end] = [r'I-' + label] * (span-1)
            else:
                raise Exception('切分句子，标记数据出现错误：'+sentence) # n
        except Exception as e :
            raise Exception(str(e))
        # print(len(sen_label), len(sen ))
        assert  len(sen_label) == len(sen )

        res['sen'] = sen
        res['label'] = sen_label

        return res

    def read_Disk(self,data_path,is_mark=True):
        """
        从磁盘读取文件
        :param data_path: 数据路径
        :param is_mark:  是否进行标注
        :return:
        """
        try :
            with open(data_path,'r',encoding='utf-8') as fin:
                result = []
                if is_mark :
                    for line in fin:
                        res_one = self._transfor_BIOES(line)
                        result.append(res_one)
                else:  # test.txt
                    for line in fin :
                        res_one = []
                        for char in line.strip() :
                            res_one.append(char)
                        result.append({'sen':res_one,'label':[]})
                return result
        except Exception as e :
            raise Exception(str(e))

    def save_Disk(self,source_path ,target_path,is_mark=True):
        """
        将源文件数据转成 BIOES格式数据
        :param source_path:  读取数据地址
        :param target_path:  保存数据地址
        :param is_mark :  数据是否进行标注
        :return:
        """
        try:
            result = []
            result = self.read_Disk(data_path=source_path,is_mark=is_mark)
            with open(target_path,'w',encoding='utf-8') as fw :
                for res  in result:
                    for i in range(len(res['sen'])):
                        # print(res['sen'][i], '\t', res['label'][i])
                        if is_mark:
                            line = res['sen'][i]+'\t'+  res['label'][i]+'\n'
                        else :
                            line = res['sen'][i]+'\n'
                        fw.write(line)
                    fw.write('\n')
        except Exception as e :
            raise Exception(str(e))


if __name__ == '__main__':

    dataprocess = DataProcess()

    data_dir = baseconfig.data_dir
    train_path = os.path.join(data_dir, 'train.txt')
    test_path = os.path.join(data_dir, 'test.txt')
    dev_path = os.path.join(data_dir, 'validation.txt')
    train_format_path = os.path.join(data_dir, 'trainFormat.txt')
    dev_format_path = os.path.join(data_dir, 'validationFormat.txt')
    test_format_path = os.path.join(data_dir, 'testFormat.txt')

    dataprocess.save_Disk(dataprocess.train_path,dataprocess.train_format_path,is_mark=True)
    dataprocess.save_Disk(dataprocess.dev_path,dataprocess.dev_format_path,is_mark=True)
    dataprocess.save_Disk(dataprocess.test_path,dataprocess.test_format_path,is_mark=False)