# modules in standard library
import base64
import re
import time
import random
from collections import Counter
from urllib.parse import urlparse
from lib.base import match_subdomains
import aiohttp
import asyncio
from lib.base import *

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
        self.headers = request_headers

    async def get_by_baidu(self):
        """
        通过百度搜索子域名
        :return: 搜索到的子域名集合
        """
        subdomains = []
        MAX_DOMAINS = 50    # 限制寻找的域名数，节约时间
        timeout = aiohttp.ClientTimeout(total=3)    # 请求超时时间2s
        base_url = 'https://www.baidu.com/s?wd={query}&oq={query}'
        prev_query = None
        count = 100  # 最多搜count次

        # 无限循环查询（被反爬虫无法翻页，利用googlehacker语法排除已经搜索到的结果来实现过滤搜索结果不断查询下去）
        while count > 0:

            if subdomains:
                fmt = 'site:{domain} -site:www.{domain} -{found}'
                found = ' -'.join(['"' + i.strip(self.domain) + '"' for i in subdomains[:MAX_DOMAINS]])
                query = fmt.format(domain=self.domain, found=found)
            else:
                query = "site:{domain} -site:www.{domain}".format(domain=self.domain)

            # 如果这次搜索的关键字和上次一样则结束搜索
            if query == prev_query:
                info(f"baidu found {len(subdomains)} domains")
                return subdomains

            # 向百度发起搜索请求
            url = base_url.format(query=query)
            try:
                async with aiohttp.request("GET", url=url, headers=self.headers, timeout=timeout) as r:
                    text = await r.text()
            except Exception as e:
                info(f"baidu timeout! May need a larger timeout")
                text = None

            # 实现从网页解析出搜索结果的url
            subdomains = match_subdomains(self.domain, subdomains, text)

            # 如果目前结果数量已经超过最大值则结束搜索
            if len(subdomains) >= MAX_DOMAINS:
                info(f"baidu found {len(subdomains)} domains")
                return subdomains

            count -= 1
            # 保留查询字符串用于判断是否停止搜索
            prev_query = query

        info(f"baidu found {len(subdomains)} domains")
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
        MAX_PAGES = 200
        timeout = 25
        base_url = "http://google.com/search?q={query}&hl=en-US&gbv=2&start={page_no}&sa=N&ved=2ahUKEwiyxO_NibzvAhVSx4sKHYDWBNQ4ChDw0wN6BAgCEEc&biw=1536&bih=378"
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
        MAX_PAGES = 500
        timeout = 25
        base_url = "https://search.yahoo.com/search?p={query}&b={page_no}"
        querydomain = self.domain

        # 无限循环翻页
        while flag:
            query = ""
            if subdomains and querydomain != self.domain:
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
                resp = self.session.get(url, headers=self.headers, timeout=timeout, proxies=proxies)
            except Exception:
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
                links = link_regx.findall(text)
                links2 = link_regx2.findall(text)
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

    async def get_by_bing(self):
        """
        通过必应搜索子域名
        :return: 搜索到的子域名集合
        """
        subdomains = []
        MAX_DOMAINS = 50
        timeout = aiohttp.ClientTimeout(total=3)
        base_url = ['https://cn.bing.com/search?q={query}&go=Submit', 'https://www.bing.com/search?q={query}&go=Submit']
        i = 0
        prev_query = None
        count = 100  # 最多搜count次

        # 无限循环查询（被反爬虫无法翻页，利用googlehacker语法排除已经搜索到的结果来实现过滤搜索结果不断查询下去）
        while count > 0:

            if subdomains:
                fmt = 'site:{domain} -site:www.{domain} -{found}'
                found = ' -'.join(['"' + i.strip(self.domain) + '"' for i in subdomains[:MAX_DOMAINS]])
                query = fmt.format(domain=self.domain, found=found)
            else:
                query = "site:{domain} -site:www.{domain}".format(domain=self.domain)

            # 如果这次搜索的关键字和上次一样则结束搜索
            if query == prev_query:
                info(f"bing found {len(subdomains)} domains")
                return subdomains

            # 向必应发起搜索请求
            url = base_url[i].format(query=query)
            try:
                async with aiohttp.request("GET", url=url, headers=self.headers, timeout=timeout) as r:
                    text = await r.text()

            except:
                text = None

            if text == None:
                i = (i + 1) % 2
                url = base_url[i].format(query=query)
                try:
                    async with aiohttp.request("GET", url=url, headers=self.headers, timeout=timeout) as r:
                        text = await r.text()
                except:
                    info(f"bing timeout! May need a larger timeout")
                    text = None

            # 实现从网页解析出搜索结果的url
            subdomains = match_subdomains(self.domain, subdomains, text)


            # 如果目前结果数量已经超过最大值则结束搜索
            if len(subdomains) >= MAX_DOMAINS:
                info(f"bing found {len(subdomains)} domains")
                return subdomains

            count -= 1
            # 保留查询字符串用于判断是否停止搜索
            prev_query = query

        info(f"bing found {len(subdomains)} domains")
        return subdomains

    def get_by_fofa(self):
        """
        通过必应搜索子域名
        :return: 搜索到的子域名集合
        """
        engine_name = "FOFA"
        flag = True
        page_no = 0
        prev_links = []
        retries = 0
        subdomains = []
        MAX_DOMAINS = 2
        MAX_PAGES = 20
        timeout = 25
        searchbs64 = ""
        base_url = "https://fofa.so/result?&qbase64=" + searchbs64
        querydomain = self.domain

        # 无限循环翻页
        while flag:
            query = ""
            searchbs64 = (str(base64.b64encode({query}.encode('utf-8')), 'utf-8'))
            if subdomains and querydomain != self.domain:
                found = ' -site:'.join(querydomain)
                query = "site:{domain} -site:www.{domain} -site:{found} ".format(domain=self.domain, found=found)
            else:
                query = "domain={domain}".format(domain=self.domain)
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

            # 向FOFA发起搜索请求
            url = base_url.format(query=query, page_no=page_no)
            try:
                resp = self.session.get(url, headers=self.headers, timeout=timeout)
            except Exception:
                resp = None

            if resp is None:
                text = 0
            text = resp.text if hasattr(resp, "text") else resp.content

            # 实现从网页解析出子域名，等同于extract_domains(DOAMIN)
            links = list()
            found_newdomain = False
            subdomain_list = []
            link_regx = re.compile('<a target="_blank" href=".*?">(.*?)<i class=".*?">...</i></a>')
            try:
                links = link_regx.findall(text)
                for link in links:
                    if not link.startswith('http'):
                        link = "http://" + link
                    subdomain = urlparse(link).netloc
                    if subdomain.endswith(self.domain):
                        subdomain_list.append(subdomain)
                        if subdomain not in subdomains and subdomain != self.domain:
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
            time.sleep(random.randint(2, 5))

        return subdomains

    def get_by_ask(self):
        """
        用ask搜索引擎
        https://www.ask.jp/
        :return:
        """
        subdomains = []

        return subdomains

def main(domain):
    """
    主函数，只需执行它就能get子域名
    :param domain:
    :return:
    """
    search_engine = SearchEngine(domain)
    # set = search_engine.get_by_baidu()
    # set = search_engine.get_by_google()
    set = search_engine.get_by_bing()

    # async函数不能直接运行，需要在事件循环里运行
    task = asyncio.ensure_future(set)   # 异步执行函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print(task.result())
    return


if __name__ == '__main__':
    # 自己在这个文件里尝试好，能获取子域名就提交上来
    main("baidu.com")    # 输出hubu.edu.com的子域名
