# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.exceptions import DropItem


class CleanTextPipeline:

    @staticmethod
    def _clean_text(text):
        return text.lower()

    def process_item(self, item, spider):
        for section in ['lead', 'text_blob', 'title']:
            item[section] = self._clean_text(item[section])
        return item
