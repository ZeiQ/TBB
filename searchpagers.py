#coding=utf8
import sys
import urllib2
#from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import re
import json
#import lxml


def MakeURL(q, s):
    '''
    The TaoBaoBroochURL looks like that:
    https://s.taobao.com/search
    ?q=%E8%83%B8%E9%92%88
    &stats_click=search_radio_all%3A1
    &ie=utf8
    &s=0
    '''
    params = ('q=%s'%q, 'stats_click=search_radio_all%3A1', 'ie=utf8', 's=%s'%s)
    taoBaoBroochURL = 'https://s.taobao.com/search?%s&%s&%s&%s'%params
    return taoBaoBroochURL
    
    
def GenURLParams(pagerNum):
    s = 44*pagerNum
    return s


def ExtractJSONData(html):
    pattern = re.compile('^g_page_config = {(.+)};$')
    lines = html.split('\n')
    for line in lines:
        line = line.strip()
        m = pattern.match(line)
        if m:
            gPageConfigString = '{' + m.group(1) + '}'
            j = json.loads(gPageConfigString)
            return j
    return None
    '''
    auctions = j['mods']['itemlist']['data']['auctions']
    for item in auctions:
        try:
            print item['raw_title'], item['view_price'], item['view_sales']
        except KeyError:
            pass
            #print item
    '''


def GetPager(pagerNum, pagerURL): 
    request = urllib2.Request(pagerURL)
    request.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0')
    reader= urllib2.urlopen(request)
    html_doc = reader.read()
    data = ExtractJSONData(html_doc)
    return (html_doc, data)
    '''
    if ExtractJSONData(html_doc):
        htm = open(r'/home/hadoop/Documents/TaobaoBrooch/pager_%s'%pagerNum, 'wb')
        htm.write(html_doc)
        htm.close()
        return True
    else:
        htm = open(r'/home/hadoop/Documents/TaobaoBrooch/error_pager_%s'%pagerNum, 'wb')
        htm.write(html_doc)
        htm.close()
        return False
    '''
    
    
def Main(jsonFilePath, pagersPath, errorPagersPath, pagersNum):
    q = '%E8%83%B8%E9%92%88' #胸针
    datas = []
    if pagersNum > 100:
        pagersNum = 100
    elif pagersNum <= 0:
        pagersNum = 1
    for n in range(0, pagersNum):
        url = MakeURL(q, GenURLParams(n))
        print url
        result = GetPager(n, url)
        html_doc = result[0]
        data = result[1]
        if data:
            htm = open(r'%s/pager_%s'%(pagersPath, n+1), 'wb')
            htm.write(html_doc)
            htm.close()
            datas.append(data)
            if n != pagersNum-1:
                sleepTime = uniform(3, 5)
                print 'Done! pager %s. Now sleep %s sec......'%(n+1, sleepTime)
                sleep(sleepTime)
            elif n == pagersNum-1:
                print 'Done! pager %s.'%pagersNum
        else:
            htm = open(r'%s/pager_%s'%(errorPagersPath, n+1), 'wb')
            htm.write(html_doc)
            htm.close()
            print 'Damned! pager %s download ERROR.'%n+1
            sleep(3)
    jsonFile = open(jsonFilePath, 'wb')
    jsonFile.write(json.dumps(datas))
    jsonFile.close()

    
if __name__ == '__main__':
    jsonFilePath = sys.argv[1]
    pagersPath = sys.argv[2]
    errorPagersPath = sys.argv[3]
    Main(jsonFilePath, pagersPath, errorPagersPath, 5)
    
    
    
    
        

