from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#测试爬取单个公众号里面的历史文章
url = 'https://mp.weixin.qq.com/profile?src=3&timestamp=1527751724&ver=1&signature=B8LotqP-Y1OqKIEnKb*NccVMGWVZQLBCuEvFgxrTLOIqUu84EGU0I7CgzD27a1CqT52mgjWYJ5XnAELZ83RfRA=='
browser = webdriver.Chrome()
browser.set_window_size(600, 600)
browser.get(url)
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#history'))
)
html = browser.page_source.replace('xmlns', 'another_attr')
doc = pq(html)
articles = doc("#history .weui_msg_card").items()
writings = {
    'update': None,

}
for item in articles:
    #print(item)
    update = item('.weui_msg_card_hd').text()
    article_url = 'http://mp.weixin.qq.com' + item('.weui_media_title').attr('hrefs')
    title = item('.weui_media_title').text()
    statement = item('.weui_media_desc').text()
    print(title)
    print(statement)
    print(article_url)
    print(update)
