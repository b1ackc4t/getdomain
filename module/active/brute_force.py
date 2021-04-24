import socket
import sys
from lib.base import *
from config.active import dns_servers
import aiodns
import asyncio
import traceback


class BruteForce:
    """
    暴力破解
    """

    def __init__(self, target, dicts_path):
        """
        初始化基本信息
        友情提示：这种注释不用手敲的，等你打好参数，写好return，再到函数第一行敲三个引号回车自动生成
        :param target: 要扫描的目标域名
        """
        self.target = target
        self.dicts_path = dicts_path
        self.resolver_timeout = 2
        self.loop = asyncio.get_event_loop()
        self.resolver = None

    def load_dict(self):
        dicts = []
        with open(self.dicts_path, encoding='utf-8') as f:
            for line in f:
                line = line.strip().lower()
                dicts.append(line)
        info(f"already load {len(dicts)}")
        return dicts

    def check_dns_servers(self):
        """
        检查dns服务器是否可用，并挑选出可用的dns服务器
        :return: 可用dns的列表
        """
        info(f"checking whether all dns servers is available")
        nice_dns_servers = []
        msg = b'\x5c\x6d\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x05baidu\x03com\x00\x00\x01\x00\x01'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(3)
        for dns_server in dns_servers:
            for i in range(2):
                sock.sendto(msg, (dns_server, 53))
                try:
                    sock.recv(4096)
                    nice_dns_servers.append(dns_server)
                    break
                except socket.timeout as e:
                    print("timeout fail!!!")
                if i == 2:
                    info(f"dns_server {dns_server} is bad!")
        return nice_dns_servers

    async def query(self, sub):
        """"""
        ret = None
        sub = ''.join(sub.rsplit(self.target, 1)).rstrip('.')
        sub_domain = f"{sub}.{self.target}"
        try:
            ret = await self.resolver.query(sub_domain, 'A')
        except aiodns.error.DNSError as e:
            err_code, err_msg = e.args[0], e.args[1]
            # 1:  DNS server returned answer with no data
            # 4:  Domain name not found
            # 11: Could not contact DNS servers
            # 12: Timeout while contacting DNS servers
            if err_code not in [1, 4, 11, 12]:
                # info(f"{sub_domain} {e}")
                pass
        except Exception as e:
            # info(sub_domain)
            # info(traceback.format_exc())
            pass
        else:
            ret = [r.host for r in ret]
            domain_ips = [s for s in ret]
            info(sub_domain + " " + str(ret))
        return sub_domain, ret


    def run(self):

        dicts = self.load_dict()
        # print(dicts)
        dns_servers = self.check_dns_servers()
        info(f"available dns_servers: {dns_servers}")
        # for dns_server in dns_servers:
        self.resolver = aiodns.DNSResolver(loop=self.loop, nameservers=dns_servers, timeout=self.resolver_timeout)
        tasks = [asyncio.ensure_future(self.query(sub)) for sub in dicts]
        done, pending = self.loop.run_until_complete(asyncio.wait(tasks))
        # info(f"@{dns_server} {done}")




def main():
    brute_force = BruteForce("baidu.com", "../../data/dict/names.txt")
    brute_force.run()


if __name__ == '__main__':
    main()
