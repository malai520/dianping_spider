import csv
import json
import os


class CSV:
    FIELDNAMES = {
        'search': [
            '店铺id', '店铺名', '评论总数', '人均价格', '标签1', '标签2',
            '店铺地址', '详情链接', '图片链接', '店铺均分', '推荐菜',
            '店铺总分', '店铺电话', '其他信息', '优惠券信息',
            '店铺纬度', '店铺经度',
        ],
        'detail': [
            '店铺id', '店铺名', '评论总数', '人均价格', '店铺地址',
            '店铺电话', '其他信息', '店铺总分', '店铺均分',
            '店铺纬度', '店铺经度',
        ],
        'review': [
            '店铺id', '评论摘要', '评论总数', '好评个数', '中评个数',
            '差评个数', '带图评论个数', '精选评论', '推荐菜',
        ],
    }

    def __init__(self, output_dir='./output'):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_data(self, data, data_type):
        if data_type not in self.FIELDNAMES:
            raise ValueError(f'不支持的数据类型：{data_type}')
        if data is None:
            return
        rows = data if isinstance(data, list) else [data]
        file_path = os.path.join(self.output_dir, f'{data_type}_res.csv')
        file_exists = os.path.exists(file_path) and os.path.getsize(file_path) > 0
        fieldnames = self.FIELDNAMES[data_type]

        with open(file_path, 'a', encoding='utf-8-sig', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction='ignore')
            if not file_exists:
                writer.writeheader()
            for row in rows:
                if not isinstance(row, dict):
                    raise TypeError('CSV 保存器只接受字典或字典列表')
                writer.writerow({key: self._serialize(row.get(key, '')) for key in fieldnames})

    @staticmethod
    def _serialize(value):
        if isinstance(value, (dict, list, tuple)):
            return json.dumps(value, ensure_ascii=False, separators=(',', ':'))
        return value
