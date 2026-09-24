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


class MongoSaver():
    def __init__(self):
        mongo_url = spider_config.MONGO_PATH
        if not mongo_url:
            raise RequestFailedError('save_mode=mongo 时必须配置 mongo_path')
        try:
            import pymongo
            client = pymongo.MongoClient(mongo_url, serverSelectionTimeoutMS=3000)
            client.admin.command('ping')
            self.database = client['dianping']
        except Exception as exc:
            raise RequestFailedError('无法连接 MongoDB，请检查 mongo_path 和服务状态') from exc

    def save_data(self, data, data_type):
        """
        保存数据
        :param data:
        :param data_type:
        :return:
        """
        assert data_type in ['search', 'detail', 'review']
        if data_type == 'search':
            self.save_search_list(data)
        elif data_type == 'detail':
            self.save_detail_list(data)
        elif data_type == 'review':
            self.save_review_list(data)
        else:
            raise Exception

    def save_search_list(self, data):
        """
        保存搜索结果
        :param data:
        :return:
        """
        col = self.database['info']
        col.delete_many({'店铺id': data['店铺id']})
        col.insert_one(data)


    def save_detail_list(self, data):
        """
        保存详细结果
        :param data:
        :return:
        """
        col = self.database['info_detail']
        col.delete_many({'店铺id': data['店铺id']})
        col.insert_one(data)


    def save_review_list(self, data):
        """
        保存评论数据
        :param data:
        :return:
        """
        col = self.database['review']
        col.delete_many({'店铺id': data['店铺id']})
        col.insert_one(data)
