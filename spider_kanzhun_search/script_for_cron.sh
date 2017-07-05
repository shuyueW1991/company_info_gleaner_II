#!/bin/sh
echo "hi, pretty~" > logpretty.txt
/usr/local/bin/scrapy crawl kanzhun_search > logfile 2>&1