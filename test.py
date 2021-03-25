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
        #通过百度搜索子域名
        #:return: 搜索到的子域名集合
        """
        engine_name = "Baidu"
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
            flag = False


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
        engine_name = "Google"
        flag = True
        page_no = 0
        prev_links = []
        retries = 0
        subdomains = []
        MAX_DOMAINS = 11
        MAX_PAGES = 20
        timeout = 25
        base_url = "http://google.com/search?q={query}&btnG=Search&hl=en-US&biw=&bih=&gbv=1&start={page_no}&filter=0"
        querydomain = self.domain

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

            # 向Google发起搜索请求
            url = base_url.format(query=query, page_no=page_no)
            proxies = {"http":"127.0.0.1:7890"}
            try:
                resp = self.session.get(url, headers=self.headers, timeout=timeout , proxies=proxies)
            except Exception:
                resp = None

            if resp is None:
                text = 0
            text = resp.text if hasattr(resp, "text") else resp.content
            print(text)
            # 实现从网页解析出子域名，等同于extract_domains(DOAMIN)
            links = list()
            link_regx = re.compile('<cite class=".*?">(.*?)</div>')
            try:
                links = link_regx.findall(text)
                for link in links:
                    link = re.sub('<span.*>', '', link)
                    if not link.startswith('http'):
                        link = "http://" + link
                    subdomain = urlparse(link).netloc
                    if subdomain and subdomain not in subdomains and subdomain != self.domain:
                        subdomains.append(subdomain.strip())
            except Exception:
                pass
            links = links

            # check if there is any error occured
            err_flag = None
            if (type(resp) is str or type(resp) is str) and 'Our systems have detected unusual traffic' in resp:
                print("[!] Error: Google probably now is blocking our requests")
                print("[~] Finished now the Google Enumeration ...")
                err_flag = False
            else:
                err_flag = True

            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no += 10

        # make another retry maybe it isn't the last page
                if retries >= 3:
                    return subdomains

            prev_links = links
            #time.sleep(5)

        return subdomains


    def get_by_Yahoo(self):
        """
        通过雅虎搜索子域名
        :return: 搜索到的子域名集合
        """
        engine_name = "Yahoo"
        flag = True
        page_no = 0
        prev_links = []
        retries = 0
        subdomains = []
        MAX_DOMAINS = 10
        MAX_PAGES = 0
        timeout = 250
        base_url = "https://search.yahoo.com/search?p={query}&b={page_no}"
        querydomain = self.domain

        # 无限循环翻页
        while flag:
            query = ""
            if subdomains:
                fmt = 'site:{domain} -domain:www.{domain} -domain:{found}'
                found = ' -domain:'.join(self.subdomains[:77])
                query = fmt.format(domain=self.domain, found=found)
            else:
                query = "site:{domain}".format(domain=self.domain)
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


            #向雅虎发起搜索请求
            url = base_url.format(query=query, page_no=page_no)
            proxies = {"http": "127.0.0.1:7890"}
            try:
                print(url)
                resp = self.session.get(url, headers=self.headers, timeout=timeout,proxies=proxies)
            except Exception as e:
                print(e)
                resp = None
            # return self.get_response(resp)

            if resp is None:
                text = 0
            text = resp.text if hasattr(resp, "text") else resp.content

            # 实现从网页解析出子域名，等同于extract_domains(DOAMIN)
            links = list()
            link_regx2 = re.compile('<span class=" fz-.*? fw-m fc-12th wr-bw.*?">(.*?)</span>')
            link_regx = re.compile('<span class="txt"><span class=" cite fw-xl fz-15px">(.*?)</span>')
            try:
                links = link_regx.findall(resp)
                links2 = link_regx2.findall(resp)
                links = links + links2
                for link in links:
                    link = re.sub("<(\/)?b>", "", link)
                    if not link.startswith('http'):
                        link = "http://" + link
                    subdomain = urlparse(link).netloc
                    if not subdomain.endswith(self.domain):
                        continue
                    if subdomain and subdomain not in subdomains and subdomain != self.domain:
                        subdomains.append(subdomain.strip())
            except Exception:
                pass
            links = links

            # if the previous page hyperlinks was the similar to the current one, then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no += 10

                # make another retry maybe it isn't the last page
                if retries >= 3:
                    return subdomains

            prev_links = links

        return subdomains



def main(domain):
    """
    主函数，只需执行它就能get子域名
    :param domain:
    :return:
    """
    search_engine = SearchEngine(domain)
    #set1 = search_engine.get_by_baidu()
    # set2 = search_engine.get_by_google()
    set3 = search_engine.get_by_Yahoo()

    return set3


if __name__ == '__main__':
    # 自己在这个文件里尝试好，能获取子域名就提交上来
    print(main("hubu.edu.cn"))    # 输出hubu.edu.com的子域名
