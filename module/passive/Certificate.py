from __future__ import print_function
import ssl
import sys
import urllib.request
import urllib.parse
import re
try:
    import OpenSSL as openssl
except ImportError:
    raise ImportError('pyopenssl library missing. pip install pyopenssl')
    sys.exit(1)


class Certificate():
    def __init__(self,url):
        self.domain_list = []
        self.cert = ''
        self.domain = ''
        self.url = url

    def get_san(self):
        cert = ssl.get_server_certificate((self.url, 443))
        x509 = openssl.crypto.load_certificate(openssl.crypto.FILETYPE_PEM, cert)
        for i in range(0, x509.get_extension_count()):
            ext = x509.get_extension(i)
            if "subjectAltName" in str(ext.get_short_name()):
                    content = ext.__str__()
                    for d in content.split(","):
                        self.domain_list.append(d.strip()[4:])
        return self.domain_list

    def getsrtsh(self,domain_list):

        with urllib.request.urlopen('https://crt.sh/?q=' + urllib.parse.quote('%.' + self.url)) as f:
                code = f.read().decode('utf-8')
                for cert, domain in re.findall(
                        '<tr>(?:\s|\S)*?href="\?id=([0-9]+?)"(?:\s|\S)*?<td>([*_a-zA-Z0-9.-]+?\.' + re.escape(
                                self.url) + ')</td>(?:\s|\S)*?</tr>', code, re.IGNORECASE):
                    domain = domain.split('@')[-1]
                    if not domain in domain_list:
                        self.domain_list.append(domain)
        return self.domain_list

    def print_domains(self,domain_list):
        if len(domain_list) > 1:
            for domain in domain_list:
                print(domain)

def main(url):
        certificate=Certificate(url)
        domain_list = certificate.getsrtsh(certificate.get_san())
        return domain_list

if __name__ == '__main__':
    print(main('hubu.edu.cn'))