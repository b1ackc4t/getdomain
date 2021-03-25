import urllib.request
import urllib.parse
import re
from lib.base import *


class Certificate():
    """
    利用证书透明度查找子域名，公开的证书查询网站
    """
    def __init__(self,url):
        self.domain_list = []
        self.domain = ''
        self.url = url

    def get_crtsh(self):
        """
        爬取crt.sh的信息
        :return: 查询到的子域名
        """
        with urllib.request.urlopen('https://crt.sh/?q=' + urllib.parse.quote('%.' + self.url)) as f:
                code = f.read().decode('utf-8')
                for cert, domain in re.findall(
                        '<tr>(?:\s|\S)*?href="\?id=([0-9]+?)"(?:\s|\S)*?<td>([*_a-zA-Z0-9.-]+?\.' + re.escape(
                                self.url) + ')</td>(?:\s|\S)*?</tr>', code, re.IGNORECASE):
                    domain = domain.split('@')[-1]
                    if not domain in self.domain_list:
                        self.domain_list.append(domain)
        return self.domain_list

    def print_domains(self,domain_list):
        if len(domain_list) > 1:
            for domain in domain_list:
                print(domain)


def main(url):
        certificate=Certificate(url)
        domain_list = certificate.get_crtsh()
        info(f"crt.sh found {len(domain_list)} subdomains")
        return domain_list

if __name__ == '__main__':
    print(main('hubu.edu.cn'))
