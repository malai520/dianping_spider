# -*- coding:utf-8 -*-

"""
      ┏┛ ┻━━━━━┛ ┻┓
      ┃　　　　　　 ┃
      ┃　　　━　　　┃
      ┃　┳┛　  ┗┳　┃
      ┃　　　　　　 ┃
      ┃　　　┻　　　┃
      ┃　　　　　　 ┃
      ┗━┓　　　┏━━━┛
        ┃　　　┃   神兽保佑
        ┃　　　┃   代码无BUG！
        ┃　　　┗━━━━━━━━━┓
        ┃CREATE BY SNIPER┣┓
        ┃　　　　         ┏┛
        ┗━┓ ┓ ┏━━━┳ ┓ ┏━┛
          ┃ ┫ ┫   ┃ ┫ ┫
          ┗━┻━┛   ┗━┻━┛

"""
from utils.spider_config import spider_config
from utils.errors import RequestFailedError


class Saver():
    """
    存储器
    """

    def __init__(self):
        self.save_mode = spider_config.SAVE_MODE
        self.saver_list = None

    def _initialize(self):
        if self.saver_list is not None:
            return
        self.saver_list = []
        # 构造每个存储方法的存储器
        if 'csv' in self.save_mode:
            from utils.saver.csv_saver import CSV
            self.saver_list.append(CSV())
        if 'mongo' in self.save_mode:
            from utils.saver.mongo_saver import MongoSaver
            self.saver_list.append(MongoSaver())
        if not self.saver_list:
            raise RequestFailedError(f'没有可用的保存器：save_mode={self.save_mode or "<empty>"}')

    def save_data(self, data, data_type):
        """
        保存数据
        :param data:
        :param data_type:
        :return:
        """
        if data_type not in ['search', 'detail', 'review']:
            raise ValueError(f'不支持的数据类型：{data_type}')
        self._initialize()
        for each in self.saver_list:
            each.save_data(data, data_type)


saver = Saver()
