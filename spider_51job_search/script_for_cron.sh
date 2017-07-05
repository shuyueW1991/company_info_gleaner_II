#!/bin/sh
echo "hi, pretty~" > logpretty.txt
/usr/local/bin/scrapy crawl search_51job > logfile 2>&1

