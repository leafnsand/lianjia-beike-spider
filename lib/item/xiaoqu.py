#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 小区信息的数据结构


class XiaoQu(object):
    def __init__(self, district, area, name, price, on_sale, year, code, mark):
        self.mark = mark
        self.code = code
        self.district = district
        self.area = area
        self.price = price
        self.name = name
        self.on_sale = on_sale
        self.year = year

    def text(self):
        return  self.mark + "," + \
                self.code + "," + \
                self.district + "," + \
                self.area + "," + \
                self.name + "," + \
                self.price + "," + \
                self.year + "," + \
                self.on_sale + "\n"

