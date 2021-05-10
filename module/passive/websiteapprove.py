#coding:utf-8
import requests
import re



class WebsiteApprove(object):
    def __init__(self,domain):
        self.domain = domain
        self.brodomain = []
        self.apikey = ''
        self.companyname = self.get_companyname()

    def get_companyname(self):
        try:
            url = f'http://apidata.chinaz.com/CallAPI/Domain?key={self.apikey}&domainName={self.domain}'
            resp = requests.get(url)
            companyname = re.findall("\"CompanyName\":\"(.*?)\",", resp.text)[0]
            #print(companyname)
        except IndexError:
            print("please input apikey or do not query foreign domain")
            exit(0)
        return companyname

    def get_by_chinaz(self):
        try:
            url = f'http://apidata.chinaz.com/CallAPI/SponsorUnit?key={self.apikey}&companyName={self.companyname}'
            resp = requests.get(url)
            self.brodomain = re.findall("\"SiteDomain\":\"(.*?)\"", resp.text)
        except IndexError:
            print("please input apikey")
            exit(0)


def main(domain):
    websiteapprove = WebsiteApprove(domain)
    websiteapprove.get_by_chinaz()
    return websiteapprove.brodomain

if __name__ == '__main__':
    print(main('baidu.com'))
