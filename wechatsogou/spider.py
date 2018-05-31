import requests
import re
from urllib.parse import unquote
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from collections import OrderedDict

from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

search_gzh_type = 1 #公众号为1
search_wz_type = 2 #文章为2

def get_search_gzh_url(keyword, page=1):
    """
    拼接搜索 公众号URL

    :param keyword: 公众号名字或者微信号
    :param page: 页码
    :return: 搜索公众号的URL
    """
    assert isinstance(page, int) and page > 0
    payload = OrderedDict()
    payload['type'] = search_gzh_type
    payload['page'] = page
    payload['ie'] = 'utf8'
    payload['query'] = keyword

    return "http://weixin.sogou.com/weixin?{}".format(urlencode(payload))

def get_gzh_information():
    url = get_search_gzh_url('csdn')
    item = {"weixinhao": None,
            "href": None,
            "information": None
        }
    headers = {
        "Host": "weixin.sogou.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
        "Referer": "http://weixin.sogou.com/weixin?type=1&query=csdn&ie=utf8&s_from=input&_sug_=y&_sug_type_="
    }
    response = requests.get(url=url, headers=headers)
    bs = BeautifulSoup(response.text, "html.parser")
    gzh_id = re.findall("sogou_vr_11002301_box_\d", str(bs))
    for x in gzh_id:
        result = bs.find_all("li", id=x)
        for gzh in result:
            item['weixinhao'] = gzh.find("p", class_="info").find("label").text
            item['href'] = gzh.find("p", class_="tit").find("a")["href"]
            item['information'] = gzh.find("dl").find("dd").text
            # print("微信号：%s" % item['weixinhao'])
            # print("微信公众号链接：%s" % item['href'])
            # print("功能介绍：%s" % item['information'])
            # print('\n')
            yield item

def get_gzh_one_article(url):
    SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']
    browser = webdriver.PhantomJS(service_args=SERVICE_ARGS, executable_path=r'D:\Phantomjs-2.1.1\bin\phantomjs.exe')
    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#js_content'))
        )
        html = browser.execute_script('return document.documentElement.outerHTML')
        doc = pq(html)
        article = doc("#js_content p").items()
        num = 0
        for i in list(article)[3:]:
            print(i.text())
    except TimeoutException:
        return get_gzh_one_article(url)
    browser.close()

def get_gzh_article(url):
    browser = webdriver.Chrome()
    browser.set_window_size(600, 600)
    try:
        browser.get(url)
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#history'))
        )
        html = browser.page_source.replace('xmlns', 'another_attr')
        doc = pq(html)
        articles = doc("#history .weui_msg_card").items()

        for item in articles:
            # print(item)
            update = item('.weui_msg_card_hd').text()
            article_url = 'http://mp.weixin.qq.com' + item('.weui_media_title').attr('hrefs')
            title = item('.weui_media_title').text()
            statement = item('.weui_media_desc').text()
            print(title)
            print(statement)
            print(article_url)
            print(update)
            get_gzh_one_article(article_url)
            print('---------\n')
    except TimeoutException:
        print("内容违规")
    browser.close()


item = get_gzh_information()
for i in item:
    print(i['weixinhao'])
    get_gzh_article(i['href'])
