
/mnt/qinzhihao/search/
说明：在招聘网站上搜索关键词，返回搜索到的企业名称和信息
输入：关键字，关键字在每个爬虫文件夹下的script_for_cron.sh文件中改
输出：公司民称、公司介绍、职位介绍，输出的文件名以website_keyword_date.csv，输出到/mnt/qinzhihao/urlcrawl/下

/mnt/qinzhihao/urlcrawl/
说明：整合所有爬虫输出的结果、去百度上用公司全称搜索官网地址、并将这两个部分的结果merge起来
输入：爬虫输出的企业信息文件
输出：整合数据输出的结果在/mnt/qinzhihao/urlcrawl/company_info_for_selection_date.csv，作为百度爬虫的输入，百度爬虫的输出为/mnt/qinzhihao/urlcrawl/urlcrawler.txt，merge两者后，结果一输出到/mnt/qinzhihao/urlcrawl/old/company_info_for_selection_date.csv，此文件作为直接发送给人工处理的结果之一，二输出到/mnt/qinzhihao/textcrawl/url_list_short.txt，作为textcrawler的输入

/mnt/qinzhidao/textcrawl/
说明：爬取官网内容和联系方式的爬虫，输入为url_list_short.txt，输出为官网文本(没有把联系方式趴下来，联系方式爬虫在spider_official_websites)
输入：url_list_short.txt
输出：/mnt/qinzhihao/textcrawl/spidername_date.txt，输出的内容是官网的文本

运行方法：sh crawl.sh，其中frontera部分需要先将strategy/db worker运行起来，一般等待爬虫爬完需要7个小时，或者使用目前被注释掉的部分，自动判断爬虫是否爬取完成，然后进行下一步。
