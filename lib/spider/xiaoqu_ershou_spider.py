#!/usr/bin/env python
# coding=utf-8
# author: zengyuetian
# 此代码仅供学习与交流，请勿用于商业用途。
# 爬取二手房数据的爬虫派生类

import re
import threadpool
from bs4 import BeautifulSoup
from lib.item.ershou import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version

XIAOQU = []

class XiaoQuErShouSpider(BaseSpider):
    def collect_xiaoqu_ershou_data(self, city_name, xiaoqu_id, fmt="csv"):
        csv_file = self.today_path + "/{0}.csv".format(xiaoqu_id)
        with open(csv_file, "w") as f:
            # 开始获得需要的板块数据
            ershous = self.get_xiaoqu_ershou_info(city_name, xiaoqu_id)
            # 锁定，多线程读写
            if self.mutex.acquire(1):
                self.total_num += len(ershous)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for ershou in ershous:
                    # print(date_string + "," + xiaoqu.text())
                    f.write(self.date_string + "," + ershou.text() + "\n")
        print("Finish crawl xiaoqu: " + xiaoqu_id + ", save data to : " + csv_file)

    @staticmethod
    def get_xiaoqu_ershou_info(city_name, xiaoqu_id):
        total_page = 1

        ershou_list = list()
        page = 'http://{0}.{1}.com/ershoufang/c{2}/'.format(city_name, SPIDER_NAME, xiaoqu_id)
        print(page)  # 打印版块页面地址
        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数，通过查找总页码的元素信息
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(xiaoqu_id))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for num in range(1, total_page + 1):
            page = 'http://{0}.{1}.com/ershoufang/c{2}/pg{3}'.format(city_name, SPIDER_NAME, xiaoqu_id, num)
            print(page)  # 打印每一页的地址
            headers = create_headers()
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elements = soup.find_all('li', class_="clear")
            for house_elem in house_elements:
                total_price_elem = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                desc = house_elem.find('div', class_="houseInfo")
                pic = house_elem.find('a', class_="img").find('img', class_="lj-lazy")

                total_price = total_price_elem.strip()
                price
                name
                house_type
                house_size
                house_dir


                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                desc = desc.text.replace("\n", "").strip()
                pic = pic.get('data-original').strip()
                # print(pic)


                # 作为对象保存
                ershou = XiaoQuErShou(chinese_district, chinese_area, name, price, desc, pic)
                ershou_list.append(ershou)

        return ershou_list

    def start(self):
        city = get_city()
        self.today_path = create_date_path("{0}/ershou".format(SPIDER_NAME), city, self.date_string)

        t1 = time.time()  # 开始计时

        # 准备线程池用到的参数
        nones = [None for i in range(len(XIAOQU))]
        city_list = [city for i in range(len(XIAOQU))]
        args = zip(zip(city_list, XIAOQU), nones)

        # 针对每个小区写一个文件,启动一个线程来操作
        pool_size = thread_pool_size
        pool = threadpool.ThreadPool(pool_size)
        my_requests = threadpool.makeRequests(self.collect_xiaoqu_ershou_data, args)
        [pool.putRequest(req) for req in my_requests]
        pool.wait()
        pool.dismissWorkers(pool_size, do_join=True)  # 完成后退出

        # 计时结束，统计结果
        t2 = time.time()
        print("Total crawl {0} xiaoqu.".format(len(XIAOQU)))
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))


if __name__ == '__main__':
    pass
