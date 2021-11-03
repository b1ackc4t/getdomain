# modules in standard library
import re
from urllib.parse import urlparse

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys #需要引入 keys 包
import time

class DnsRecord(object):
    def __init__(self, domain):
        """
        初始化基本信息
        :param target: 要扫描的目标域名
        """

        self.domain = domain
        self.session = requests.Session()
        self.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.8',
        'Accept-Encoding': 'gzip',
        }


    def get_by_hackertarget(self):

        subdomains = []

        base_url="https://hackertarget.com/find-dns-host-records/"
        #driver = webdriver.Chrome()
        driver = webdriver.Firefox()   #打开浏览器
        #driver.get("http://www.baidu.com")
        driver.get(base_url)   #打开网页
        #通过name方式定位
        driver.find_element_by_name("theinput").send_keys(self.domain)    #定位输入查询域名
        #time.sleep(3)
        #driver.maximize_window()   #浏览器全屏显示

        driver.find_element_by_name("theinput").send_keys(Keys.ENTER)    #定位键盘操作，查询
        time.sleep(3)

        text = driver.find_element_by_id("formResponse").text   #包括域名和IP
        links = list()
        link_regx = re.compile('(.*?)'+self.domain+'')   #匹配域名
        links = link_regx.findall(text)



        try:
            for link in links:
                if not link.startswith('http'):
                    link = "http://" + link + self.domain
                subdomain = urlparse(link).netloc
                if subdomain not in subdomains and subdomain != self.domain:
                    subdomains.append(subdomain.strip())
        except Exception:
            pass

        return subdomains
        driver.quit()

def main(domain):
    """
    主函数，只需执行它就能get子域名
    :param domain:
    :return:
    """
    dns_record = DnsRecord(domain)
    set1 = dns_record.get_by_hackertarget()
    return set1



if __name__ == '__main__':
    # 自己在这个文件里尝试好，能获取子域名就提交上来
    print(main("hubu.edu.cn"))    # 输出hubu.edu.com的子域名