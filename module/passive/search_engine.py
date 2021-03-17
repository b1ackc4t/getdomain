# modules in standard library
import re
import time
import random
from collections import Counter
from urllib.parse import urlparse

# external modules
import requests


class SearchEngine(object):
    """
    通过“”“搜索引擎”“”公开搜索子域名
    已包含的搜索引擎：
    google
    baidu
    shodan
    fofa
    """

    def __init__(self, domain):
        """
        初始化基本信息
        友情提示：这种注释不用手敲的，等你打好参数，写好return，再到函数第一行敲三个引号回车自动生成
        :param target: 要扫描的目标域名
        """

        self.engine_name = "Baidu"
        self.domain = domain
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip',
        }


    def get_by_baidu(self):
        """
        通过百度搜索子域名
        :return: 搜索到的子域名集合
        """
        flag = True
        page_no = 0
        prev_links = []
        retries = 0
        subdomains = []
        MAX_DOMAINS = 2
        MAX_PAGES = 70
        timeout = 25
        base_url = 'https://www.baidu.com/s?pn={page_no}&wd={query}&oq={query}'
        querydomain = self.domain

        # 无限循环翻页
        while flag:
            query = ""
            if subdomains and querydomain != self.domain:
                found = ' -site:'.join(querydomain)
                query = "site:{domain} -site:www.{domain} -site:{found} ".format(domain=self.domain, found=found)
            else:
                query = "site:{domain} -site:www.{domain}".format(domain=self.domain)
            count = query.count(self.domain)  # finding the number of subdomains found so far

            # if they we reached the maximum number of subdomains in search query
            # then we should go over the pages
            do_flag = None
            if MAX_DOMAINS == 0:
                do_flag = False
            else:
                do_flag = count >= MAX_DOMAINS

            if do_flag:
                page_no += 10

            pn_flag = None
            if MAX_PAGES == 0:
                pn_flag = False
            else:
                pn_flag = page_no >= MAX_PAGES

            if pn_flag:  # maximum pages for Google to avoid getting blocked
                return subdomains

            # 向百度发起搜索请求
            url = base_url.format(query=query, page_no=page_no)
            try:
                resp = self.session.get(url, headers=self.headers, timeout=timeout)
            except Exception:
                resp = None
            # return self.get_response(resp)

            if resp is None:
                text = 0
            text = resp.text if hasattr(resp, "text") else resp.content


            # 实现从网页解析出子域名，等同于extract_domains(DOAMIN)
            links = list()
            found_newdomain = False
            subdomain_list = []
            link_regx = re.compile('<a.*?class="c-showurl.*?".*?>(.*?)</a>')
            try:
                links = link_regx.findall(text)
                for link in links:
                    link = re.sub('<.*?>|>|<|&nbsp;', '', link)
                    if not link.startswith('http'):
                        link = "http://" + link
                    subdomain = urlparse(link).netloc
                    if subdomain.endswith(self.domain):
                        subdomain_list.append(subdomain)
                        if subdomain not in subdomains and subdomain != self.domain:
                            found_newdomain = True
                            subdomains.append(subdomain.strip())
            except Exception:
                pass
            if not found_newdomain and subdomain_list:
                count = Counter(subdomains)
                subdomain1 = max(count, key=count.get)
                count.pop(subdomain1, "None")
                subdomain2 = max(count, key=count.get) if count else ''
                querydomain = (subdomain1, subdomain2)
                # querydomain = self.findsubs(subdomain_list)
            links = links
           # links = self.extract_domains(resp)

            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no += 10


        # make another retry maybe it isn't the last page
                if retries >= 3:
                    return subdomains

            prev_links = links
            # time.sleep(random.randint(2, 5))



        return subdomains

    def get_by_google(self):
        """
        通过谷歌搜索子域名
        :return: 搜索到的子域名集合
        """
        subdomains = set()
        return subdomains

    # 其他各种函数已省略


def main(domain):
    """
    主函数，只需执行它就能get子域名
    :param domain:
    :return:
    """
    search_engine = SearchEngine(domain)
    set1 = search_engine.get_by_baidu()

    return set1


if __name__ == '__main__':
    # 自己在这个文件里尝试好，能获取子域名就提交上来
    print(main("hubu.edu.cn"))    # 输出hubu.edu.com的子域名
