from logging import info
import requests
import re



class ThreatCrowd(object):
    def __init__(self,domain):
        """
        利用威胁情报网站查询子域名
        """
        self.domain = domain
        self.subdomians = []

    def match_subdomains(self, resp):
        '''
        匹配子域名
        '''
        result = re.findall(r'(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.){0,}' \
                 + self.domain.replace('.', r'\.'), resp, re.I)
        for subdoamin in result:
            subdoamin = subdoamin.split('@')[-1]
            if not subdoamin in self.subdomians:
                self.subdomians.append(subdoamin)


    def get_by_alien(self):
        '''
        返回子域名
        '''
        dns = f'https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns'
        resp = requests.get(dns)
        dns_subdomains = self.match_subdomains(resp.text)
        self.subdomians.append(dns_subdomains)

        url = f'https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/url_list'
        resp = requests.get(url)
        url_subdomains = self.match_subdomains(resp.text)
        self.subdomians.append(url_subdomains)
        return self.subdomians



def main(domain):
    threatcrowd = ThreatCrowd(domain)
    subdomains = threatcrowd.get_by_alien()
    info(f"alienvault found {len(subdomains)} subdomains")
    return subdomains

if __name__ == '__main__':
    print(main('hubu.edu.cn'))
