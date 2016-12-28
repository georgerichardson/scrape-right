# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import arrow
from scrapy.exceptions import DropItem


class ValidateRequiredFields:
    def process_item(self, item, spider):
        required = ['language', 'url', 'text_blob', 'source']
        missing = []
        for field in required:
            if field not in item:
                missing.append(field)
        if missing:
            raise DropItem("Missing required field: {}".format(missing))
        return item


class CleanTextPipeline:

    @staticmethod
    def _clean_text(text):
        return text.lower()

    def process_item(self, item, spider):
        for section in ['lead', 'text_blob', 'title']:
            if section in item:
                item[section] = self._clean_text(item[section])
        return item


class StandardizeDatetime:

    @staticmethod
    def _standardize_datetime(text):
        time = arrow.get(text)
        return time.naive

    def process_item(self, item, spider):
        for date_field in ['pub_datetime', 'modified_datetime']:
            if date_field in item:
                item[date_field] = self._standardize_datetime(item[date_field])
        return item
