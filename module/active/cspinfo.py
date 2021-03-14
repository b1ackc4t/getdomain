from requests import get, exceptions
from tldextract import extract
import asyncio
import aiohttp

class CSPInfo:
    """
    利用csp头搜集子域名
    """

    def __init__(self, url):
        """
        :param apex_domain: csp头中对应的顶级域名
        :param ip: 域名对应ip地址
        :param count: 域名有几个子域名
        :param status: 域名是否可访问
        :param url: 网址
        """
        self.apex_domain = ""
        self.ip = ""
        self.count = ""
        self.status = True
        self.url = url
        self.csp_header = ''
        self.sub_domains = set()

    # def create_url(self):
    #     """
    #     通过域名创建url， 并设置状态码
    #     """
    #     url_append = ["http://", "https://"]
    #     for ua in url_append:
    #         url_test = ua + self.domain
    #         r = get(url_test)
    #         if r.status_code == 200:
    #             self.url = url_test
    #     self.status = False

    async def get_csp_header(self):
        """
        获取url的csp头
        """
        try:
            async with aiohttp.request('HEAD', url=self.url, headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36'}) as r:
                await r.read()
        except exceptions.RequestException as e:
            print(e)

        if 'Content-Security-Policy' in r.headers:
            csp_header = r.headers['Content-Security-Policy']
            self.csp_header = csp_header
            self.get_sub_domains()
        elif 'Content-Security-Policy-report-only' in r.headers:
            csp_header = r.headers['Content-Security-Policy-report-only']
            self.csp_header = csp_header
            self.get_sub_domains()
        else:
            self.status = False

    def get_sub_domains(self):
        """
        从csp头部获取未处理过的url列表
        对其列表进行清理，提取子域名
        存放在self.sub_domains
        """
        csp_sub_domains = []
        csp_header_list = self.csp_header.split(" ")
        for line in csp_header_list:
            if "." in line:
                line = line.replace(';', '')
                csp_sub_domains.append(line)
            else:
                pass
        # 进行清理
        # print(csp_sub_domains)
        domain_ext = extract(self.url)
        for csp_url in csp_sub_domains:
            ext = extract(csp_url)
            if ext[0] not in ['*', ''] and ext[1] == domain_ext[1] and ext[2] == domain_ext[2]:
                self.sub_domains.add('.'.join(ext))
        # print(self.sub_domains)


async def main(url):
    """
    供调用的接口
    :param url: 传入要识别csp的url
    :return: 获取到的子域名集合
    """
    # 建立对象
    csp_info = CSPInfo(url)

    # 获取目标url的csp头
    await asyncio.ensure_future(csp_info.get_csp_header())
    # 获取子域名
    # print(csp_info.sub_domains)
    return csp_info.sub_domains

    # dns解析
    # if resolve:
    # domains = resolve_domains(domains)
    # 查看whois信息
    # if check_whois:
    # domains = check_whois_domains(domains)


if __name__ == '__main__':
    # print(main("http://flipkart.com"))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main("http://flipkart.com"))  # 处理一个任务

