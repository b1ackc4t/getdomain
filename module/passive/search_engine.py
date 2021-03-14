import sys


class SearchEngine:
    """
    通过搜索引擎公开搜索子域名
    已包含的搜索引擎：
    google
    baidu
    shodan
    fofa
    """

    def __init__(self, target):
        """
        初始化基本信息
        友情提示：这种注释不用手敲的，等你打好参数，写好return，再到函数第一行敲三个引号回车自动生成
        :param target: 要扫描的目标域名
        """
        self.target = target

    def get_by_baidu(self):
        """
        通过百度搜索子域名
        :return: 搜索到的子域名列表
        """
        domain_li = []
        return domain_li

    def get_by_google(self):
        """
        通过谷歌搜索子域名
        :return: 搜索到的子域名列表
        """
        domain_li = []
        return domain_li


if __name__ == '__main__':
    search_engine = SearchEngine("xxx.com")
    search_engine.get_by_baidu()    # 自己测试好功能是否可用
