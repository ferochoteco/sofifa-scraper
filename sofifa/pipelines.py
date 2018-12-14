# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class SofifaPipeline(object):
#     def __init__(self):
#         ''''
#         teams = {
#             '10': {
#                     210257:{},
#             }
#         }
#         '''
#         self.teams = {}
#         self.players = []
#
#     def open_spider(self, spider):
#         for team in spider.team_id_list:
#             self.teams[team] = {}
#
#     def process_item(self, item, spider):
#         #self.teams[item.get('team_id')][item.get('player_id')] = item
#         self.players.append(item)
#
#         return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w+b')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        line = json.dumps(dict(item)) + ",\n"
        self.file.write(line)
        return item



