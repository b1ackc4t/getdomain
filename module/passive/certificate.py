import urllib.request
import urllib.parse
import re


class Certificate():
    def __init__(self,url):
        self.domain_list = []
        self.domain = ''
        self.url = url

    def get_crtsh(self):
        with urllib.request.urlopen('https://crt.sh/?q=' + urllib.parse.quote('%.' + self.url)) as f:
                code = f.read().decode('utf-8')
                for cert, domain in re.findall(
                        '<tr>(?:\s|\S)*?href="\?id=([0-9]+?)"(?:\s|\S)*?<td>([*_a-zA-Z0-9.-]+?\.' + re.escape(
                                self.url) + ')</td>(?:\s|\S)*?</tr>', code, re.IGNORECASE):
                    domain = domain.split('@')[-1]
                    if not domain in self.domain_list:
                        self.domain_list.append(domain)
        return self.domain_list

    def print_domains(self,domain_list):
        if len(domain_list) > 1:
            for domain in domain_list:
                print(domain)

def main(url):
        certificate=Certificate(url)
        domain_list = certificate.get_crtsh()
        return domain_list

if __name__ == '__main__':
    print(main('hubu.edu.cn'))
