#!/bin/sh
echo "hi, pretty~" > logpretty.txt
/usr/local/bin/scrapy crawl lpsearch -a searchword=海外 > logfile 2>&1

