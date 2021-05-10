import re
import requests

class WhoisReverse(object):
    def __init__(self,domain):
        '''
        :param domain:
        '''
        self.domain = domain
        self.url = 'http://whois.bugscaner.com/'
        self.email_url = 'http://whois.bugscaner.com/email/'
        self.match_email = "\"/emailtoimage/(.*?)\">"
        self.match_brodomain = '</th>\\n<td><a href=\"/(.*?)\"'
        self.match_nextpage = '\"Next\" href=\"/email/(.*?)\"'
        self.brodomain = []
        self.email_code = self.get_emailcode()

    def get_emailcode(self):
        resp = requests.get(self.url + self.domain)
        email_code = re.findall(self.match_email,resp.text)[0]
        return email_code

    def get_brodomain(self):
        resp = requests.get(self.email_url + self.email_code).text
        self.brodomain += re.findall(self.match_brodomain,resp)

        #翻页
        while(1):
            next_page = re.findall(self.match_nextpage, resp)
            #print(next_page)
            if len(next_page) != 0:#如果有就翻页，没有就结束
                resp = requests.get(self.email_url + next_page[0]).text

                self.brodomain += re.findall(self.match_brodomain, resp)
            else:
                break


def main(domain):
    whoisreverse = WhoisReverse(domain)
    whoisreverse.get_brodomain()
    return whoisreverse.brodomain

if __name__ == '__main__':
    print(main('baidu.com'))

