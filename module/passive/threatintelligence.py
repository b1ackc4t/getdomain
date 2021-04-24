import requests
import re
from logging import info

class ThreatIntelligence(object):
    def __init__(self,domain):
        """
        利用威胁情报网站查询子域名
        """
        self.domain = domain
        self.subdomians = []
        self.x_apikey = ''
        self.apikey = ""

    def match_subdomains(self,domain, subdomians, resp):
        '''
        匹配子域名
        '''

        result = re.findall(r'(?:[a-z0-9](?:[a-z0-9\-]{1,61}[a-z0-9])?\.){1,}' \
                            + domain.replace('.', r'\.'), resp, re.I)
        for subdoamin in result:
            subdoamin = subdoamin.split('@')[-1]
            if not subdoamin in subdomians:
                subdomians.append(subdoamin)
        return subdomians

    def get_by_alexa(self):
        url = 'https://alexa.chinaz.com/'+self.domain
        resp = requests.get(url)
        self.subdomians = self.match_subdomains(self.domain, self.subdomians, resp.text)
        return self.subdomians

    def get_by_alien(self):
        '''
        返回子域名
        '''
        dns = f'https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns'
        resp = requests.get(dns)
        dns_subdomains = self.match_subdomains(self.domain,self.subdomians,resp.text).pop()
        self.subdomians.append(dns_subdomains)

    def get_by_threatbook(self):
        url = "https://api.threatbook.cn/v3/domain/sub_domains"
        query = {
            "apikey": self.apikey,
            "resource": self.domain
        }
        if len(self.apikey) == 0: return  self.subdomians
        resp = requests.request("GET", url, params=query)
        self.subdomians = self.match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

    def get_by_threatminer(self):
        url = 'https://api.threatminer.org/v2/domain.php?q={0}&rt=5'.format(self.domain)
        resp = requests.get(url).text
        self.subdomians = self.match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

    def get_by_virutotal(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
            'x-apikey': self.x_apikey
        }
        if len(self.x_apikey) == 0: return self.subdomians
        url = 'https://www.virustotal.com/api/v3/domains/{0}/subdomains'.format(self.domain)
        resp = requests.request("GET", url, headers = headers).text
        self.subdomians = self.match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

def main(domain):
    threatintelligence = ThreatIntelligence(domain)
    threatintelligence.get_by_alien()
    threatintelligence.get_by_alexa()
    threatintelligence.get_by_virutotal()
    threatintelligence.get_by_threatminer()
    subdomains = threatintelligence.get_by_threatbook()
    info(f"virustotal found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('hubu.edu.cn'))
