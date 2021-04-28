import requests
from logging import info
from lib.base import match_subdomains

class Virustotal(object):
    def __init__(self,domain):
        self.domain = domain
        self.subdomians = []
        self.x_apikey = ''

    def get_by_virutotal(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 Safari/537.36 SE 2.X MetaSr 1.0',
            'x-apikey': self.x_apikey
        }
        if len(self.x_apikey) == 0: return ''
        url = 'https://www.virustotal.com/api/v3/domains/{0}/subdomains'.format(self.domain)
        resp = requests.request("GET", url, headers = headers).text
        self.subdomians = match_subdomains(self.domain, self.subdomians, resp)
        return self.subdomians

def main(domain):
    virustotal = Virustotal(domain)
    subdomains = virustotal.get_by_virutotal()
    info(f"virustotal found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('aliyun.com'))
