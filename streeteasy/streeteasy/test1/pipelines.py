# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import csv

class Test1Pipeline(object):
    def __init__(self):
        self.fp = open('house_info_jump.csv', 'w', encoding='utf-8',newline='')
        self.headers = [
            'building_name','unit', 'beds','baths', 'price','url_py'
        ]
        self.writer = csv.DictWriter(self.fp, self.headers)
        self.writer.writeheader()

    def process_item(self, item, spider):
        self.ITEM = []
        self.ITEM.append(item)
        self.writer.writerows(self.ITEM)
        return item

    def close_spider(self,spider):
        self.fp.close()



# import json


# class Test1Pipeline(object):
#     def __init__(self):
#         self.file = None
#
#     def open_spider(self,spider):
#         try:
#             self.file = open("Test1Item.json", "w", encoding="utf-8")
#         except Exception as err:
#             print(err)
#
#     def process_item(self, item, spider):
#         dict_item = dict(item)
#         json_str = json.dumps(dict_item, ensure_ascii=False) + "\n"
#         self.file.write(json_str)
#         return item
#
#     def close_spider(self, spider):
#         self.file.close()
