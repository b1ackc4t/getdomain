import re
import requests
import os

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
        self.key = ''
        self.whoisre_enable = True


    def getbrodomain_by_bugscaner(self):
        resp = requests.get(self.url + self.domain)
        #print(resp.text)
        registrars = re.findall('的注册商(.*?),', resp.text)
        email_code = re.findall(self.match_email, resp.text)

        if len(email_code) !=0:
            resp = requests.get(self.email_url + email_code[0]).text
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

    def getbrodomain_by_chinaz(self):
        url = 'http://apidata.chinaz.com/CallAPI/Whois?key='+self.key+'&domainName='+self.domain
        resp = requests.get(url).text
        registrar = re.findall('\"Registrar\":\" (.*?)\"', resp)
        phone = re.findall('\"Phone\":\"(.*?)\"', resp)
        email = re.findall('\"Email\":\"(.*?)\"', resp)
        if registrar != 0:
            f = open(os.getcwd() + r'\sub-discovery\Acc.txt', encoding='utf-8').read().strip()#域名商合集

            if f.find(registrar[0]) >= 0:  #如果在文件中找到，说明是注册商管理，就无法通过whois反查
                self.whoisre_enable = False
                return 0

            registrar_url = 'http://apidata.chinaz.com/CallAPI/WhoisReverse?key=' + self.key + '&queryData=' + registrar[0] + '&queryType=Registrant'
            resp = requests.get(registrar_url).text
            self.brodomain += re.findall('\"Host\":\"(.*?)\"', resp)

        if email != 0:
            email_url = 'http://apidata.chinaz.com/CallAPI/WhoisReverse?key=' + self.key + '&queryData=' + email[0] + '&queryType=Email'
            resp = requests.get(email_url).text
            self.brodomain += re.findall('\"Host\":\"(.*?)\"', resp)

        if phone != 0 :
            phone_url = 'http://apidata.chinaz.com/CallAPI/WhoisReverse?key=' + self.key + '&queryData=' + phone[0] + '&queryType=Phone'
            resp = requests.get(phone_url).text
            self.brodomain += re.findall('\"Host\":\"(.*?)\"', resp)


            registrar_url = 'http://apidata.chinaz.com/CallAPI/WhoisReverse?key=' + self.key + '&queryData=' + registrar[0] + '&queryType=Registrant'




def main(domain):
    whoisreverse = WhoisReverse(domain)
    whoisreverse.getbrodomain_by_chinaz()
    whoisreverse.getbrodomain_by_bugscaner()
    return whoisreverse.brodomain

if __name__ == '__main__':
    print(main('baidu.com'))

