# python 3.6
# author: qcw

from requests import get, exceptions
import re


class SentiveFile(object):
    """
    从可能泄露的敏感文件中发现子域名，如crossdomain.xml、robots.txt等等
    """

    def __init__(self, url):
        self.url = url
        self.domains = set()

    CROSS_DOMAIN_XML = """<?xml version="1.0"?>
    <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
    <cross-domain-policy>
        <allow-access-from domain="localhost:3001" />
    </cross-domain-policy>
    """

    def get_sentive_message(self):
        files = [
            "/crossdomain.xml",
            "/robot.txt"
        ]
        res_access = r'<allow-access-from domain="(.*?)"'
        domain = ''
        try:
            for file in files:
                r = get(self.url + file)
                domain = re.findall(res_access, r.text)
                if len(domain) != 0:
                    for i in range(len(domain)):
                        self.domains.add(domain[i])
        except exceptions.RequestException as e:
            print(e)
        print(self.domains)


def main(url):
    # 建立对象
    sentive_file = SentiveFile(url)
    # 获取页面内容中敏感信息
    sentive_file.get_sentive_message()


if __name__ == '__main__':
    main("http://www.sina.com.cn")
