# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2022/6/4 17:22
# @Author  : xiaoxiaoshutong
# @Email   : ****
# @Site    :
# @File    : test.py
# @Software: PyCharm
# 子系统
class CPU:
    def run(self):
        print('cpu run')
    def stop(self):
        print('cpu stop')
class Disk:
    def run(self):
        print('Disk run')
    def stop(self):
        print('Disk stop')
class Memory:
    def run(self):
        print('Memory run')
    def stop(self):
        print('Memory stop')

 # 外观 facade
class Computer:
    def __init__(self):
        self.cpu = CPU()
        self.disk = Disk()
        self.memory = Memory()
    def run(self):
        self.cpu.run()
        self.disk.run()
        self.memory.run()
    def stop(self):
        self.cpu.stop()
        self.memory.stop()
        self.disk.stop()

#client
computer = Computer()
computer.run()
computer.stop()