#coding=utf8
import json
import urllib2
#from bs4 import BeautifulSoup
import os
import sys
from time import sleep
from random import uniform
from selenium import webdriver
import re


class HTTPRedirectHandlerMore(urllib2.HTTPRedirectHandler):
    # maximum number of redirections to any single URL
    # this is needed because of the state that cookies introduce
    max_repeats = 8
    # maximum total number of redirections (regardless of URL) before
    # assuming we're in a loop
    max_redirections = 20
    
    
def Download(URL):
    request = urllib2.Request(URL)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
    opener = urllib2.build_opener(HTTPRedirectHandlerMore)
    content = opener.open(request)
    return content.read()

    
def ExtractElementsOnDetail(driver, wantedElements):
    '''
    wantedElements looks like that:
    {
    'monthly_sales': ('//li[@data-label="月销量"]/div/span[@class="tm-count"]', None),
    'total_comment': ('//li[@id="J_ItemRates"]/div/span[@class="tm-count"]', None),
    'collect_count': ('//li[@data-label="月销量"]/div/span[@class="tm-count"]', u'^（([0-9]+)人气）$')
    ｝
    '''
    elements = {}
    for wantedElementName in wantedElements.keys():
        xpath = wantedElements[wantedElementName][0]
        if wantedElements[wantedElementName][1]:
            pattern = re.compile(wantedElements[wantedElementName][1])
        else:
            pattern = None
        element = driver.find_element_by_xpath(xpath)
        if pattern:
            m = pattern.match(element.text)
            if m:
                elementText = m.group(1)
            else:
                elementText = None
        else:
            elementText = element.text
        elements[wantedElementName] = elementText
    return elements
        
    
def ExtractDetails(detailPagerURL):
    driver = webdriver.PhantomJS(executable_path=r'/usr/local/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    #driver = webdriver.Firefox()
    driver.get(detailPagerURL)
    if driver.current_url.startswith('https://detail.tmall.com'):
        wantedElements = {'monthly_sales': ('//li[@data-label="月销量"]/div/span[@class="tm-count"]', None), \
                          'total_comment': ('//li[@id="J_ItemRates"]/div/span[@class="tm-count"]', None), \
                          'collect_count': ('//span[@id="J_CollectCount"]', u'^（([0-9]+)人气）$')}
    elif driver.current_url.startswith('https://item.taobao.com'):
        wantedElements = {'monthly_sales': ('//li[@id="J_Counter"]/div[@class="tb-counter-bd"]/div[@class="tb-sell-counter"]/a/strong[@id="J_SellCounter"]', None), \
                          'total_comment': ('//li[@id="J_Counter"]/div[@class="tb-counter-bd"]/div[@class="tb-rate-counter"]/a/strong[@id="J_RateCounter"]', None), \
                          'collect_count': ('//li[@class="tb-social-fav"]/a[@shortcut-label="收藏宝贝"]/em[@class="J_FavCount"]', u'^\(([0-9]+)人气\)$')}
    else:
        wantedElements = None
    if wantedElements:
        elements = ExtractElementsOnDetail(driver, wantedElements)
    else:
        elements = None
    if elements:
        driver.quit()
        return elements
    else:
        print 'Can not extract details from ' + driver.title + '!'
        driver.quit()
        return None
        

def ExtractData(originalItem):
    if originalItem.has_key('activity'):
        return None
    else:
        item = {}
        item['nid'] = originalItem['nid']
        item['category'] = originalItem['category']
        item['pid'] = originalItem['pid']
        item['title'] = originalItem['title']
        item['raw_title'] = originalItem['raw_title']
        if originalItem['pic_url'].startswith('https:') or originalItem['pic_url'].startswith('http:'):
            item['pic_url'] = originalItem['pic_url']
        elif originalItem['pic_url'].startswith('//'):
            item['pic_url'] = 'https:' + originalItem['pic_url']
        else:
            raise
        if originalItem['detail_url'].startswith('https:') or originalItem['detail_url'].startswith('http:'):
            item['detail_url'] = originalItem['detail_url']
        elif originalItem['detail_url'].startswith('//'):
            item['detail_url'] = 'https:' + originalItem['detail_url']
        else:
            raise
        item['view_price'] = originalItem['view_price']
        item['view_fee'] = originalItem['view_fee']
        item['item_loc'] = originalItem['item_loc']
        item['reserve_price'] = originalItem['reserve_price']
        item['view_sales'] = originalItem['view_sales']
        item['comment_count'] = originalItem['comment_count']
        item['user_id'] = originalItem['user_id']
        item['nick'] = originalItem['nick']
        if item['pic_url'].startswith('https:') or item['pic_url'].startswith('http:'):
            pic = Download(item['pic_url'])
        else:
            pic = Download(r'https:' + item['pic_url'])
        details = ExtractDetails(item['detail_url'])
        if details:
            item['monthly_sales'] = details['monthly_sales']
            item['total_comment'] = details['total_comment']
            item['collect_count'] = details['collect_count']
        return (item, pic) 
    
    
def Main(oriDataPathName, exItemsPathName, exItemPicsPath):
    if os.path.exists(exItemPicsPath) and os.path.isdir(exItemPicsPath):
        pass
    else:
        os.mkdir(exItemPicsPath)
    datafile = open(oriDataPathName, 'rb')
    data = datafile.read()
    pagers = json.loads(data)
    pagerNum = 0
    items = []
    for pager in pagers:
        pagerNum += 1
        auctions = pager['mods']['itemlist']['data']['auctions']
        itemNum = 0
        for originalItem in auctions:
            itemNum += 1
            try:
                print 'Handle Pager %s, Item %s'%(pagerNum, itemNum)
                exData = ExtractData(originalItem)
                item = exData[0]
                pic = exData[1]
                picPath = exItemPicsPath + r'/pic_%s_%s'%(pagerNum, itemNum)
                picFile = open(picPath, 'wb')
                picFile.write(pic)
                picFile.close()
                items.append(item)
                print 'Detail URL is ' + item['detail_url'] + '\n' + 'Detail title is ' + item['title'] + \
                u', 月销量：' + item['monthly_sales'] + u', 累计评论：' + item['total_comment'] + u', 收藏：' + item['collect_count'] + '.'
                sleepTime = uniform(1, 2)
                print 'Now sleep %s sec......'%sleepTime
                sleep(sleepTime)
            except KeyError:
                #pass
                print originalItem
    datafile.close()
    newItemsFile = open(exItemsPathName, 'wb')
    newItemsFile.write(json.dumps(items))
    newItemsFile.close()
    

if __name__ == '__main__':
    oriDataPathName = sys.argv[1]
    exItemsPathName = sys.argv[2]
    exItemPicsPath = sys.argv[3]
    Main(oriDataPathName, exItemsPathName, exItemPicsPath)
    
    print 'Done!'
    
    
    
    
    
    
    
