#coding=utf8
from selenium import webdriver
import re

#driver = webdriver.PhantomJS(executable_path=r'/home/hadoop/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
driver = webdriver.Firefox()
#driver.implicitly_wait(10)
#driver.get("https://detail.tmall.com/item.htm?id=38871530740&ali_refid=a3_430585_1006:1109351313:N:%E8%83%B8%E9%92%88:635ceaa9d452ef4ff0565b61ac02762c&ali_trackid=1_635ceaa9d452ef4ff0565b61ac02762c")
#driver.get("https://click.simba.taobao.com/cc_im?p=%D0%D8%D5%EB&s=841002890&k=333&e=Tg8coCBP0L4qhCIre%2FiorX9c7SqOVeTPYBRzlA3IV80JtfVZUp%2BF2mHiykPOXOGWuPFUQWg72U%2BK4ympmOPPXldCMjXeQOkesp7t1GQLHjbFYGppqWdDiWDFY2dxeRjC9vSIC87D4xbD0t9Dx1PtE4nu%2BMgmkmdcQek2b3rjx230dqo4JgzYQyuYyhUMqAYOI6p1WseVl1p1NIh%2BV3ZDsfM%2FqeiksfRf%2B7R3BmlZGmAb%2BHuftZtyhX7NF9zhJNSOl98y2X2KBRQF7UKrPIhFy5tdqBFS%2FXwDl6cDg6l01RIkJDQuN2TtZbwd96YIefQgjgJekU%2FEobw%3D")
driver.get("https://item.taobao.com/item.htm?id=16817007085&ns=1&abbucket=0#detail")
print driver.title
collectCount = driver.find_element_by_xpath('//li[@class="tb-social-fav"]/a[@shortcut-label="收藏宝贝"]/em[@class="J_FavCount"]')
pattern = re.compile(u'^\(([0-9]+)人气\)$')
m = pattern.match(collectCount.text)
if m:
    print m.group(1)
print u'人气：　' + collectCount.text


sellCount = driver.find_element_by_xpath('//li[@id="J_Counter"]/div[@class="tb-counter-bd"]/div[@class="tb-sell-counter"]/a/strong[@id="J_SellCounter"]')
print u'月销量： ' + sellCount.text
commentCount = driver.find_element_by_xpath('//li[@id="J_Counter"]/div[@class="tb-counter-bd"]/div[@class="tb-rate-counter"]/a/strong[@id="J_RateCounter"]')
print u'累计评论：　' + commentCount.text

     
if driver.current_url.startswith('https://detail.tmall.com'):
    print 'tmall'
elif driver.current_url.startswith('https://item.taobao.com'):
    print 'taobao'
driver.quit()

