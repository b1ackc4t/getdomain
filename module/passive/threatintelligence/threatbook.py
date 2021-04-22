import requests
from logging import info
from common import match_subdomains

class ThreatBook(object):
    def __init__(self,domain):
        self.domain = domain
        self.subdomians = []
        self.apikey = ""


    def get_by_threatbook(self):
        url = "https://api.threatbook.cn/v3/domain/sub_domains"
        query = {
            "apikey": self.apikey,
            "resource": self.domain
        }
        if len(self.apikey) == 0: return ''
        resp = requests.request("GET", url, params=query)
        self.subdomians = match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

def main(domain):
    threatbook = ThreatBook(domain)
    subdomains = threatbook.get_by_threatbook()
    info(f"threatbook found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('aliyun.com'))

