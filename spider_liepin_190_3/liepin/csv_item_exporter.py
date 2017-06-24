# -*- coding: utf-8 -*-
from scrapy.conf import settings
# from scrapy.contrib.exporter import CsvItemExporter
from scrapy.exporters import CsvItemExporter


class MyProjectCsvItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', ',')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])

        if fields_to_export:
            kwargs['fields_to_export'] = fields_to_export


        feed_store_empty = settings.get('FEED_STORE_EMPTY',True)
        kwargs['feed_store_empty'] = feed_store_empty

        super(MyProjectCsvItemExporter, self).__init__(*args, **kwargs)
