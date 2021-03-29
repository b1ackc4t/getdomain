# python 3.6
# author: qcw

from requests import get, exceptions
import re


class SentiveFile(object):
    """
    从可能泄露的敏感文件中发现子域名，如crossdomain.xml、robots.txt等等
    """

    def __init__(self, url):
        """
        :param url: 外部输入的url
        :param domians:返回主程序的结果
        """
        self.url = url
        self.domains = set()

    CROSS_DOMAIN_XML = """<?xml version="1.0"?>
    <!DOCTYPE cross-domain-policy SYSTEM "http://www.macromedia.com/xml/dtds/cross-domain-policy.dtd">
    <cross-domain-policy>
        <allow-access-from domain="localhost:3001" />
    </cross-domain-policy>
    """

    def get_sentive_message(self):
        """
        files列表可从外部导入文件
        爬取可能泄露信息页面中的敏感信息
        :return: self.domains
        """
        files = [
            "/crossdomain.xml",
            "/robot.txt"
        ]
        res_access = r'<allow-access-from domain="(.*?)"'
        try:
            for file in files:
                r = get(self.url + file)
                domain = re.findall(res_access, r.text)
                # ['a', 'a', 'g', 'https://baidu.com', 'http://qq.com', 'qq.com']  #
                if len(domain) != 0:
                    for i in range(len(domain)):
                        self.domains.add(domain[i])
        except exceptions.RequestException as e:
            print(e)
        print(self.domains)

    def get_clean(self):
        """
        初清洗 暂时只褪去http://
        :return:
        """
        unwashed_domains = self.domains
        cleaned_domains = set()
        for domain in unwashed_domains:
            if 'http://' in domain:
                domain = domain.replace('http://', '')
            if 'https://' in domain:
                domain = domain.replace('https://', '')
            cleaned_domains.add(domain)
        self.domains = cleaned_domains
        print(self.domains)


def main(url):
    # 建立对象
    sentive_file = SentiveFile(url)
    # 获取页面内容中敏感信息
    sentive_file.get_sentive_message()
    # 清洗数据
    sentive_file.get_clean()


if __name__ == '__main__':
    main("http://www.sina.com.cn")
