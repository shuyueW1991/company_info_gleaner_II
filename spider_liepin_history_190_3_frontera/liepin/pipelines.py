# -*- coding: utf-8 -*-
import codecs
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class LiepinPipeline(object):
    def __init__(self):
        self.file = codecs.open('liepinhistoire_data190_3_frontera.csv','a',encoding = 'utf-8')
    def process_item(self, item, spider):
        if  len(item['lp_exist']) == 0 :

            line = ''
            if  item['lp_job_id']:
                if  item['lp_job_id'][0].replace("\n","").replace("\t","").replace("\r","").replace("https://www.liepin.com/job/","").replace(".shtml",""):
                    line = line + item['lp_job_id'][0].replace("\n","").replace("\t","").replace("\r","").replace("https://www.liepin.com/job/","").replace(".shtml","")
            else:
                line = line + 'NaN'

            if  item['lp_co_nm']:
                if  item['lp_co_nm'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_co_nm'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + 'NaN'


            if item['lp_co_tag']:
                if item['lp_co_tag'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_co_tag'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_co_ownership']:
                if item['lp_co_ownership'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_co_ownership'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'
            #
            if item['lp_co_stf_num']:
                if item['lp_co_stf_num'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_co_stf_num'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'
            #
            if item['lp_co_lk']:
                if item['lp_co_lk'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_co_lk'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_co_add']:
                if item['lp_co_add'][1].replace("\n","").replace("\t","").replace("\r","").replace(" ",""):
                    line = line + '|' + item['lp_co_add'][1].replace("\n","").replace("\t","").replace("\r","").replace(" ","")
            else:
                line = line + '|' + 'NaN'


            if item['lp_job_pub_nm']:
                if item['lp_job_pub_nm'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_job_pub_nm'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'


            if item['lp_job_pub_pos']:
                if item['lp_job_pub_pos'][0].replace("\n","").replace("\t","").replace("\r","").replace("/","").replace(" ",""):
                    line = line + '|' + item['lp_job_pub_pos'][0].replace("\n","").replace("\t","").replace("\r","").replace("/","").replace(" ","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_apply_check_rate']:
                if item['lp_job_apply_check_rate'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_job_apply_check_rate'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_apply_check_dur']:
                if item['lp_job_apply_check_dur'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_job_apply_check_dur'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_nm']:
                if item['lp_job_nm'][0].replace("\n","").replace("\t","").replace("\r",""):
                    line = line + '|' + item['lp_job_nm'][0].replace("\n","").replace("\t","").replace("\r","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_salary']:
                if item['lp_job_salary'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_salary'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_apply_fdbk']:
                if item['lp_job_apply_fdbk'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_apply_fdbk'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_add']:
                if item['lp_job_add'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_add'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_pub_time']:
                if item['lp_job_pub_time'][1].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_pub_time'][1].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_quals']:
                if "/".join(item['lp_job_quals']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + "/".join(item['lp_job_quals']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'


            if item['lp_job_descr']:
                if "/".join(item['lp_job_descr']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','').replace("<br>",""):
                    line = line + '|' + "/".join(item['lp_job_descr']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','').replace("<br>","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_dept']:
                if item['lp_job_dept'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_dept'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_major']:
                if item['lp_job_major'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_major'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_boss']:
                if item['lp_job_boss'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_boss'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_job_subordinate']:
                if item['lp_job_subordinate'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"',''):
                    line = line + '|' + item['lp_job_subordinate'][0].replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','')
            else:
                line = line + '|' + 'NaN'

            if item['lp_co_intro']:
                if "/".join(item['lp_co_intro']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','').replace("<br>",""):
                    line = line + '|' + "/".join(item['lp_co_intro']).replace("\n","").replace("\t","").replace("\r","").replace(" ","").replace('"','').replace("<br>","")
            else:
                line = line + '|' + 'NaN'

            if item['lp_update_datetime']:
                if item['lp_update_datetime']:
                    line = line + '|' + item['lp_update_datetime']
            else:
                line = line + '|' + 'NaN'


            line = line+ '\n'

            self.file.write(line)
            self.file.flush()
            return item
