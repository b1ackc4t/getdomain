import re
import os



class DomainTransfer():
    def __init__(self,url):
        self.url = url
        self.cmd_res = ''
        self.dns_servers=[]

    def dns_zone_tranfer_finder(self):
        print('Nslookup %s' % self.url)
        self.cmd_res = os.popen('nslookup -type=ns ' + self.url).read()  # 获取dns服务
        dns_servers = re.findall('nameserver = ([\w\.]+)', self.cmd_res)
        if len(dns_servers) == 0:
            print('No DNS Server Found!\n')
            exit(0)
        else:
            self.get_subdomain_by_dig(dns_servers)

    def get_subdomain_by_dig(self,dns_servers):
        usage()
        for vulnerable_dns in dns_servers:
            print('Using @%s' % vulnerable_dns)
            cmd_res = os.popen('dig @%s axfr %s' % (vulnerable_dns, self.url)).read() #获取cmd中的返回值
            if cmd_res.find('XFR size') > 0:#查找有XFR字段的部分
                print('DNS Domain Transfer vulnerability found:', vulnerable_dns)
                print (cmd_res)
            else:
                print('No DNS Domain Transfer vulnerability found')


def usage():
    print('if you do not have dig')
    print('Please run  \'一键安装.bat\' in dig.x32 or dig.x64')

def main(url):
    domaintransfer=DomainTransfer(url)
    print('try to get %s DNS Server' % url)
    domaintransfer.dns_zone_tranfer_finder()

if __name__ == "__main__":
    print(main('hubu.edu.cn'))