from requests import get, exceptions
import click
from socket import gethostbyname, gaierror
from sys import version_info, exit
from tldextract import extract


class CSPInfo:
    """
    利用csp头搜集子域名
    """

    def __init__(self, domain):
        """
        :param domain: 域名
        :param apex_domain: csp头中对应的顶级域名
        :param ip: 域名对应ip地址
        :param count: 域名有几个子域名
        :param status: 域名是否可访问
        :param url: 网址
        """
        self.domain = domain
        self.apex_domain = ""
        self.ip = ""
        self.count = ""
        self.status = True
        self.url = ""
        self.csp_header = ''
        self.sub_domains = []

    def create_url(self):
        """
        通过域名创建url， 并设置状态码
        """
        url_append = ["http://", "https://"]
        for ua in url_append:
            url_test = ua + self.domain
            r = get(url_test)
            if r.status_code == 200:
                self.url = url_test
        self.status = False

    def get_csp_header(self):
        """
        获取url的csp头
        """
        try:
            r = get(self.url)
        except exceptions.RequestException as e:
            print(e)
            exit(1)
        if 'Content-Security-Policy' in r.headers:
            csp_header = r.headers['Content-Security-Policy']
            self.csp_header = csp_header
        elif 'Content-Security-Policy-report-only' in r.headers:
            csp_header = r.headers['Content-Security-Policy-report-only']
            self.csp_header = csp_header
        else:
            exit(1)
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
        for csp_url in csp_sub_domains:
            ext = extract(csp_url)
            if ext[0] in ['*', '']:
                self.apex_domain = '.'.join(ext[1:])
                csp_sub_domains.remove(csp_url)
            else:
                csp_url = '.'.join(ext)
        self.sub_domains = csp_sub_domains


def main(domain):
    # 建立对象
    csp_info = CSPInfo(domain)
    # 获取域名url
    csp_info.create_url()
    # 获取目标url的csp头
    csp_info.get_csp_header()
    # 获取子域名
    csp_info.get_sub_domains()

    # dns解析
    # if resolve:
    # domains = resolve_domains(domains)
    # 查看whois信息
    # if check_whois:
    # domains = check_whois_domains(domains)


if __name__ == '__main__':
    main("baidu.com")

