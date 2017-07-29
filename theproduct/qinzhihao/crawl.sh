SHELL=/bin/bash
PATH=/sbin:/bin:/usr/sbin:/usr/bin
# run search
cd /mnt/qinzhihao/search/spider_Chinahr_search/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_zhilian_search_needing_broadcrawling3/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_liepin_search/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_lagou_search/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_kanzhun_search/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_boss_search/;sh script_for_cron.sh &
cd /mnt/qinzhihao/search/spider_51job_search/;sh script_for_cron.sh &

#wait search
sleep 10m
#ps -ef | grep scrapy > search
#var=$(cat search | grep 'qinzh' | wc -l)
#if [ $var -gt 0 ]
#then
#    sleep 300 ; ps -ef | grep scrapy > search.log
#    var=$(cat search | grep 'qinzhi' | wc -l)
#fi

#run urlcrawler and send url
cd /mnt/qinzhihao/url_crawl/;/usr/local/bin/scrapy crawl urlcrawler
python3 data.py > log.log

#run content crawler
cd /mnt/qinzhihao/text_crawl/
python3 -m frontera.contrib.messagebus.zeromq.broker &
python3 -m frontera.worker.db --config frontier.workersettings &
scrapy crawl crawler -s SPIDER_PARTITION_ID=0 &
scrapy crawl crawler -s SPIDER_PARTITION_ID=1 &





# $ | grep -o -E '[0-9]+' | head -1 | sed -e 's/^0\+//'

#sleep 20m
#cd /mnt/qinzhihao