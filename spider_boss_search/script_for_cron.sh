#!/bin/sh
echo "hi, pretty~" > logpretty.txt
/usr/local/bin/scrapy crawl boss_search > logfile 2>&1

