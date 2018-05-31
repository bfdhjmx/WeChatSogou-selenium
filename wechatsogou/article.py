from pyquery import PyQuery as pq

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#测试单个历史文章
SERVICE_ARGS = ['--load-images=false','--disk-cache=true']
url = 'https://mp.weixin.qq.com/s?timestamp=1527751840&src=3&ver=1&signature=7tojk3mTEx5za99mHFFtVhgcclg*Rz5f8oTZ8prsZ9yHxSlfKaM5DwZYBcAhPBIl6Axpo-HgPDcJRovAt5y8Qs3*CP-u-7mQ3SO7iFrTvPL9rFN5Aq9qHscZM6wc*B3zOiy27VwiHVoP-xRE4L1ssjgwtXEJ4rpwwdFG1eJK8as='
#PhantomJS已经不支持了，可以直接换成Chrome()
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS, executable_path=r'D:\Phantomjs-2.1.1\bin\phantomjs.exe')

browser.get(url)
WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, '#js_content'))
)
html = browser.execute_script('return document.documentElement.outerHTML')
doc = pq(html)
print(html)
browser.close()
# article = doc("#js_content p").items()
# num = 0
# for i in list(article)[3:]:
#     print(i.text())
# browser.close()