# python 3.6
# author: qcw

from requests import exceptions
from urllib import request
import re
# 关键词列表建立所需要的依赖包
import pkg_resources
from symspellpy.symspellpy import SymSpell
from tldextract import extract
# 拼音
import pypinyin

PUBLIC_SUFFIX_LIST_URLS = (
    "https://publicsuffix.org/list/public_suffix_list.dat",
    "https://raw.githubusercontent.com/publicsuffix/list/master/public_suffix_list.dat",
)


class SourceCode(object):
    """
    从前端源码中可能发现子域名（html、js）（css一般不会有，不考虑）
    """

    def __init__(  # 初始值为外部的url
            self,
            url
    ):
        """
        :param urls: 外部输入的url为第一个参数，兄弟域名为第二个参数
        :param key: 外部输入的url域名关键字
        :param keys: 外部输入的url域名关键字延伸列表
        :param domain:外部网址的域名
        :param text:爬取的网页页面 str类型
        :param sub_count:发现子域名的个数
        :param bro_count:发现兄弟域名的个数
        :param status:是否发现子域名
        :param sub_domains:子域名集合
        :param bro_domains:兄弟域名集合
        """

        self.urls = [url]
        self.domain = get_domain_and_key(url)[0]
        self.key = get_domain_and_key(url)[1]
        self.keys = get_keys(self.key)
        self.text = ''
        self.sub_count = 0
        self.bro_count = 0
        self.status = True
        self.sub_domains = set()
        self.bro_domains = set()
        self.suffix_text = extract(str(url)[2])

    def get_urls(self):
        try:
            # 通过urllib获取网页源码，然后将二进制数据解析成UTF-8编码
            r = request.urlopen(self.urls[0])
            self.text += r.read().decode("UTF-8")
        except exceptions.RequestException as e:
            print(e)
            exit(1)
        res_js = r'http[s]?://[0-9-a-zA-Z+&@#/%?=~_|!:,.;]+js[0-9-a-zA-Z+&@#/%?=~_|!:,.;]+'
        urls = re.findall(res_js, self.text)
        self.urls.extend(urls)

        print(self.urls)

    def get_source(self):
        try:
            # 通过urllib获取网页源码，然后将二进制数据解析成UTF-8编码
            for i in range(1, len(self.urls)):
                r = request.urlopen(self.urls[i])
                self.text += r.read().decode("UTF-8")
        except exceptions.RequestException as e:
            print(e)
            exit(1)

    def get_sub_domains(self):
        """
        从源代码中爬取子域名
        结果:
        self.sub_domains
        self.sub_count
        """
        # 查找子域名的正则表达式
        # 不奇怪的定义域名 -0-9a-zA-Z_.
        res_access = r'[0-9-a-zA-Z+&@#%?~_|!,.;]+' + r'[.]' + self.domain
        sub_domains = re.findall(res_access, self.text)
        # 当爬取的域名列表不为空则将结果保存在self.sub_domains
        # 将列表转换为set
        self.sub_domains = set(sub_domains)
        # 统计子域名的个数
        self.sub_count = len(self.sub_domains)

    def get_bro_domains(self):
        """
        从源代码中爬取子域名
        结果:
        self.bro_domains
        self.bro_count
        """
        bro_domains = []
        for i in range(1, len(self.keys)):
            res_access = r'[0-9a-zA-Z\_\.]+' + r'[.]' + self.keys[i] + r'[0-9a-zA-Z\_\.]+'
            # 将匹配的列表结果加入bro_domains中
            bro_domains.extend(re.findall(res_access, self.text))
        # 将列表转为集合
        self.bro_domains = set(bro_domains)
        # 统计兄弟域名的个数
        self.bro_count = len(self.bro_domains)

    def get_clean_brodomains(self):
        """
        初清洗 暂时只褪去http://、未包含主域名的域名
        """
        for u in self.bro_domains.copy():
            if extract(u)[2] == '':
                self.bro_domains.remove(u)

        print(self.domain)
        print(self.key)
        print(self.keys)
        print(self.sub_domains)
        print(self.sub_count)
        print(self.bro_domains)
        print(self.bro_count)


def get_domain_and_key(url):
    """
    将url转换为domain
    :return: [domain, key]
    """
    domain = ''
    key = ''
    if 'http://' in url:
        domain = url.replace('http://', '')
    if 'https://' in url:
        domain = url.replace('https://', '')
    suffix = ['.com', '.com.cn']
    for item in suffix:
        if item in domain:
            temp = domain.replace(item, '')
            index = temp.rfind('.') + 1
            key = temp[index:]

    return domain, key


def get_keys(key):
    # 获得keys关键词延伸列表
    # 将关键词本身作为第一个列表元素加入
    keys = [key]

    # 首先对数字进行处理
    isdigit_list = re.findall(r"\d+", key)
    keys.extend(isdigit_list)
    # 去除字符串中的数字
    for i in isdigit_list:
        key = key.replace(i, '')
    # 中文拼音模糊加入keys，换取不要依赖包
    for i in range(len(key)):
        for j in range(i + 1, len(key)):
            # 双字拼音
            keys.append(key[i] + key[j])
    # 单词缩写
    sym_spell = SymSpell(max_dictionary_edit_distance=0, prefix_length=7)
    dictionary_path = pkg_resources.resource_filename("symspellpy", "frequency_dictionary_en_82_765.txt")
    sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

    # a sentence without any spaces
    result = sym_spell.word_segmentation(key)
    # print("{}, {}, {}".format(result.corrected_string, result.distance_sum, result.log_prob_sum))
    # 将分割的单词字符串转换为列表, 加入keys
    result_list = result.corrected_string.split(' ')
    keys.extend(result_list)
    # 获得首字母列表
    w_first_list = [result_list[i][0] for i in range(len(result_list))]
    # 将数字和首字母进行组合, 加入keys
    mix_list = []
    for i in isdigit_list:
        for j in w_first_list:
            temp1 = i + j
            temp2 = j + i
            mix_list.append(temp1)
            mix_list.append(temp2)
    keys.extend(mix_list)
    # 转换为单词首字母字符串, 加入keys
    w_first_str = ''.join(w_first_list)
    # print(w_first_str)
    keys.append(w_first_str)

    print(keys)

    return keys


def main(url):
    # 建立对象
    source_code = SourceCode(url)
    # 获取网页列表
    source_code.get_urls()
    # 获取源代码中其他页面的内容
    source_code.get_source()
    # 获取页面内容中的子域名
    source_code.get_sub_domains()
    # 获取页面内容中的兄弟域名
    source_code.get_bro_domains()
    # 清洗数据
    source_code.get_clean_brodomains()


if __name__ == '__main__':
    main("https://baidu.com")
