import requests
from logging import info
from lib.base import match_subdomains

class Alexa(object):
    def __init__(self,domain):
        """
        利用威胁情报网站查询子域名
        """
        self.domain = domain
        self.subdomians = []

    def get_by_alexa(self):
        url = 'https://alexa.chinaz.com/'+self.domain
        resp = requests.get(url)
        self.subdomians = match_subdomains(self.domain, self.subdomians, resp.text)
        return self.subdomians

def main(domain):
    alexa = Alexa(domain)
    subdomains = alexa.get_by_alexa()
    info(f"alexa found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('baidu.com'))