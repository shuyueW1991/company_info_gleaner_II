Running Frontera:
python3 -m frontera.contrib.messagebus.zeromq.broker
python3 -m frontera.worker.db --config frontier.workersettings

Running Crawlers:
nohup scrapy crawl zhilian -s SPIDER_PARTITION_ID=0 &
nohup scrapy crawl zhilian -s SPIDER_PARTITION_ID=1 &
