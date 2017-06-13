# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import scrapy
import re
from scrapy.exporters import CsvItemExporter
from scrapy.conf import settings
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join, Compose
from scrapy.exporters import CsvItemExporter

class DajieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    co_web_id = scrapy.Field()
    co_name = scrapy.Field()
    co_add = scrapy.Field()
    co_type = scrapy.Field()
    co_number = scrapy.Field()
    co_web_add = scrapy.Field()


def clean(x):
    x = x.replace('\t','').replace('\n','').replace('\r','').replace(" ",'').replace(' ','').replace('"','').replace('&nbsp;','')
    print(len(x))
    print(x)
    if len(x) > 0:
        return x
    else:
        return 'NaN'

def cleanhttp(x):
    if x:
        x = x.replace('\t','').replace('\n','').replace('\r','').replace(' ','').replace(' ','').replace('"','').replace('&nbsp;','')
        print(len(x))
        print(x)
        return x
    else:
        return 'NaN'


def strip_ppline_left(x):
    x = x.strip('\t').strip('\n').strip('\r').strip(" ").strip(' ').strip('"').strip('&nbsp;')
    print(len(x))
    print(x)
    if len(x) > 0:
        return x
    else:
        return 'NaN'

def void_nan(x):
    if x == None:
        return 'NaN'
        print(x)
    else:
        return x


def strip(x):
    x = x.strip()
    print(len(x))
    print(x)
    if len(x) > 0:
        return x
    else:
        return 'NaN'

def strip_type(x):
    count = len(re.findall('<label', x))
    if count == 3:
        p = re.compile(r'<label.*?/label>')
        x = p.findall(x)[-1]
        x = re.sub("<span.*?/span>","",x)
        x = re.sub('<label class="at">',"",x)
        x = re.sub("</label>","",x)
        return x
    else:
        return 'NaN'



def strip_ppline_left(x):
    x = x.strip('\t').strip('\n').strip('\r').strip(" ").strip(' ').strip('"').strip('&nbsp;')
    print(len(x))
    print(x)
    if len(x) > 0:
        return x
    else:
        return 'NaN'

def numeric_only(x):
    text = re.sub("\D","", x)
    if text:
        return str(text)
    else:
        return 'NaN'

def find_tag_ownership(x):
    if x:
        xx= x.split('|')
        return xx[0]
    else:
        return 'NaN'

def find_tag_stfnum(x):
    if x:
        xx= x.split('|')
        return xx[1]
    else:
        return 'NaN'

def find_tag_type(x):
    if x:
        xx= x.split('|')
        return xx[-1]
    else:
        return 'NaN'

def find_tag_stfnum_0(x):
    x=x.strip('<p>').strip('</p>')
    if x:
        p = re.sub("<em.*?/em>","shit",x)
        pp= p.split('shit')
        return pp[-2]
    else:
        return 'NaN'

def find_tag_type_0(x):
    x=x.strip('<p>').strip('</p>')
    if x:
        p = re.sub("<em.*?/em>","shit",x)
        pp= p.split('shit')
        return pp[-1]
    else:
        return 'NaN'


def list_string_merge(x):
    return "".join(x)


def span_regex(x):
    clean = re.search(r'<span>.*</span>',x)
    return clean.group(0).strip('<span>').strip('</span>')

def p_regex(x):
    clean = re.search(r'<p>.*</p>',x)
    return clean.group(0).strip('<p>').strip('</p>')

def mgmt_name_clean(x):
    clean = re.findall(r'"name":".+?"',x)
    return clean

def mgmt_title_clean(x):
    clean = re.findall(r'"position":".+?"',x)
    return clean

def mgmt_remark_clean(x):
    clean = re.findall(r'"remark":".+?"',x)
    return clean

def co_desc_clean(x):
    clean = re.search(r'"introduction":{.+?}',x)
    return clean.group().strip('"introduction":')

def prd_desc_clean(x):
    clean = re.findall(r'"productprofile":".+?"',x)
    return clean

def prd_name_clean(x):
    clean = re.findall(r'"product":".+?"',x)
    return clean

def position_count_clean(x):
    clean = re.search(r'"positionCount":\d+',x)
    return clean.group().strip('"positionCount":')

def resume_rate_clean(x):
    clean = re.search(r'"resumeProcessRate":\d+',x)
    return clean.group().strip('"resumeProcessRate":')

def experience_count_clean(x):
    clean = re.search(r'"experienceCount":\d+',x)
    return clean.group().strip('"experienceCount":')

def resume_time_clean(x):
    clean = re.search(r'"resumeProcessTime":\d+',x)
    return clean.group().strip('"resumeProcessTime":')

def co_id_clean(x):
    clean = re.search(r'"companyId":\d+',x)
    return clean.group().strip('"companyId":')

class TxtItemExporter(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        delimiter = settings.get('CSV_DELIMITER', '|')
        kwargs['delimiter'] = delimiter

        fields_to_export = settings.get('FIELDS_TO_EXPORT', [])
        if fields_to_export:
        	kwargs['fields_to_export'] = fields_to_export

        super(TxtItemExporter, self).__init__(*args, **kwargs)



class DajieLoader(ItemLoader):
    default_item_class = DajieItem
    default_output_processor = Join()

    #Chinahr_co_web_id_in = MapCompose(numeric_only)
    co_web_id_in = MapCompose(numeric_only)
    co_name_in = MapCompose(clean)
    co_number_in = MapCompose(clean)
    co_type_in = MapCompose(clean)
    # co_short_desc_in = MapCompose(strip)
    co_add_in = MapCompose(clean)
    co_web_add_in = MapCompose(cleanhttp)


