import sys
import io
import re

import pandas as pd
#from pyxlsb import open_workbook
import requests
import urllib.request as req
import urllib.parse as rep
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from lxml import html


'''
# base line for hangul on ATOM Editor
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')
'''

# read xlsb file https://github.com/wwwiiilll/pyxlsb
# pd.read_excel('★마담당 운영상품_180703_과일채소.xlsb')

manage_deal = pd.read_excel('★마담당 운영상품_180703_과일채소.xlsx', sheetname='★서울청과 과일').iloc[:,[1,4]]

print(manage_deal.shape)
print(manage_deal)

# Check robots.txt
# Ref: http://www.happyjung.com/lecture/258
# TEST_URL = 'https://intoli.com/blog/making-chrome-headless-undetectable/chrome-headless-test.html'

base_html = 'http://www2.ticketmonster.co.kr/mart/category/19110000' # 티몬 슈퍼마트 '과일,채소,두부' 카테고리

quote = rep.quote_plus('고당도 수박 5~6kg 1통')
search_html = 'http://search.ticketmonster.co.kr/search/?keyword=' + quote + '&thr=ts' # 키워드 검색 Page
print(search_html)

# html parsing으로는 내부 구조가 안 보인다
# Maybe, JavaScript 로 만들어져 인가??

# Selenium으로 접근하기
# Chrome Headless 만들기 --------------------------------------------------------
# https://beomi.github.io/2017/09/28/HowToMakeWebCrawler-Headless-Chrome/
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument('disable-gpu')
# UserAgent Headless 값 변경(일반적인 Chrome으로 보이기)
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36')
options.add_argument("lang=ko_KR") # Chrome 한국어 설정

print('>>>>>>>>>>>>>>>>> Connecting TMON <<<<<<<<<<<<<<<<<<')
driver = webdriver.Chrome('/Users/Chris/Downloads/chromedriver', chrome_options=options)

# # [Test] Headless 탐지 막기 >> Headless 제거 ------------------------------------------
# driver.get(TEST_URL)
#
# user_agent = driver.find_element_by_css_selector('#user-agent').text
# print('User-Agent: ', user_agent)
# driver.quit()

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# tests = soup.find_all('li', attrs={'class': 'item'})
a_tag = soup.find_all('a', attrs={'class': 'anchor'})
li_tag_price = soup.find_all('span', attrs={'class': 'sale'})

titles = []
urls = []
prices = []

# Regular Expression
# https://regexr.com/
pattern_deal_no = 'opt_deal_srl=[0-9]+'
pattern_price = '[ㄱ-힣]+:\d,\d+[원]|[ㄱ-힣]+:\d+[원]'
deal_no = re.compile(pattern_deal_no)
price_ = re.compile(pattern_price)

for a in a_tag:
    titles.append(a['title'])
    urls.append(a['href'])

split_deal_no = []
for url in urls:
    if deal_no.search(url) != None:
        deal_srl = deal_no.search(url).group()
        split_deal_no.append(deal_srl.replace('opt_deal_srl=', ''))
    else:
        split_deal_no.append(url.replace(url, 'NaN'))

for p in li_tag_price:
    prices.append(p.text)

split_price = []
for price in prices:
    if price_.search(price) != None:
        clean_price = price_.search(price).group()
        split_price.append(clean_price)
    else:
        split_price.append(price.replace(price, 'NaN'))


print('>>>>>>>>>>>>>>>>> Disconnecting TMON <<<<<<<<<<<<<<<<<<')
driver.close()
driver.quit()


print('Tilte Info')
print(titles)
print('------------------------------------------------------')
print('Deal Number')
print(split_deal_no)
print('------------------------------------------------------')
print('Price Info')
print(prices)


# # ---------- [Sample] Extracting a deal number from URL-------------------------------------------
# urls = ['http://www.ticketmonster.co.kr/deal/474556018?opt_deal_srl=539413738&keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/266338389?opt_deal_srl=307409906&keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/266338389?opt_deal_srl=307409910&keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/266338389?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/696457034?opt_deal_srl=696466710&keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/520615446?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/520615446?opt_deal_srl=520652618&keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/696457034?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/211881929?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/1394246990?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/202472773?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/362580130?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/975281102?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/1413555022?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/1421938450?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g',
#         'http://www.ticketmonster.co.kr/deal/821289642?keyword=%EB%B0%A9%EC%9A%B8%ED%86%A0%EB%A7%88%ED%86%A0+500g']
#
# print(len(urls), urls)
# print(urls[0].split('=')[1].replace('&keyword', ''))
# print([url.split('=')[1].replace('&keyword', '') for url in urls])
# print(deal_no)
# print([deal_no.search(url).group() for url in urls if deal_no.search(url) != None])
#
# test = []
# for url in urls:
#     if deal_no.search(url) != None:
#         deal_srl = deal_no.search(url).group()
#         test.append(deal_srl.replace('opt_deal_srl=', ''))
#     else:
#         test.append(url.replace(url, 'NaN'))
#
# print(len(test), test)