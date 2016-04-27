#coding=utf8
import sys
import urllib2
#from bs4 import BeautifulSoup
from time import sleep
from random import uniform
import re
import json
import lxml


def MakeURL(q, s, initID):
    '''
    The TaoBaoBroochURL looks like that:
    https://s.taobao.com/search
    ?q=%E8%83%B8%E9%92%88
    &imgfile=
    &js=1
    &stats_click=search_radio_all%3A1
    &initiative_id=staobaoz_20160402
    &ie=utf8
    &p4ppushleft=1%2C48
    &p4plefttype=3%2C1
    &p4pleftnum=1%2C3
    &s=0
    '''
    params = ('q=%s'%q, 'imgfile=', 'js=1', 'stats_click=search_radio_all%3A1', \
              'initiative_id=%s'%initID, 'ie=utf8', 'p4ppushleft=1%2C48', \
              'p4plefttype=3%2C1', 'p4pleftnum=1%2C3', 's=%s'%s)
    taoBaoBroochURL = 'https://s.taobao.com/search?%s&%s&%s&%s&%s&%s&%s&%s&%s&%s'%params
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
    
    
def Main(jsonPath, pagerPath, errorPath):
    q = '%E8%83%B8%E9%92%88' #胸针
    initID = 'staobaoz_20160403'
    datas = []
    for n in range(0, 100):
        url = MakeURL(q, GenURLParams(n), initID)
        print url
        result = GetPager(n, url)
        html_doc = result[0]
        data = result[1]
        if data:
            htm = open(r'%s/pager_%s'%(pagerPath, n+1), 'wb')
            htm.write(html_doc)
            htm.close()
            datas.append(data)
            sleepTime = uniform(5, 17)
            print 'Done! pager %s Now sleep %s sec......'%(n+1, sleepTime)
            sleep(sleepTime)
        else:
            htm = open(r'%s/pager_%s'%(errorPath, n+1), 'wb')
            htm.write(html_doc)
            htm.close()
            print 'Damned! pager %s download ERROR.'%n+1
            sleep(3)
    jsonFile = open(jsonPath, 'wb')
    jsonFile.write(json.dumps(datas))
    
    jsonFile.close()


class handler(object):
    max = 10
    
    def run(self):
        for i in range(self.max):
            print i

class handlerer(handler):
    max = 100

if __name__ == '__main__':
    '''
    jsonFile = sys.argv[1]
    pagerPath = sys.argv[2]
    errorPath = sys.argv[3]
    Main(jsonFile, pagerPath, errorPath)
    '''
    
    
    
        

