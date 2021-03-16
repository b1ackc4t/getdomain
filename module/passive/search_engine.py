import sys


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

    def get_by_baidu(self):
        """
        通过百度搜索子域名
        :return: 搜索到的子域名集合
        """
        subdomains = set()
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
    set2 = search_engine.get_by_google()

    return set1 | set2


if __name__ == '__main__':
    # 自己在这个文件里尝试好，能获取子域名就提交上来
    print(main("hubu.edu.com"))    # 输出hubu.edu.com的子域名
