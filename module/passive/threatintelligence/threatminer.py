import requests
from logging import info
from lib.base import match_subdomains

class ThreatMiner(object):
    def __init__(self,domain):
        self.domain = domain
        self.subdomians = []


    def get_by_threatminer(self):
        url = 'https://api.threatminer.org/v2/domain.php?q={0}&rt=5'.format(self.domain)
        resp = requests.get(url).text
        self.subdomians = match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

def main(domain):
    threatminer = ThreatMiner(domain)
    subdomains = threatminer.get_by_threatminer()
    info(f"threatminer found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('aliyun.com'))

