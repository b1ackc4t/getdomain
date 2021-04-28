import urllib.request
import urllib.parse
import re
import asyncio
import aiohttp
from lib.base import *


class Certificate():
    def __init__(self, domain):
        self.domain_list = []
        self.domain = domain
        self.headers = request_headers

    async def get_crtsh(self):
        timeout = aiohttp.ClientTimeout(total=4)
        try:
            async with aiohttp.request("GET", url=f"https://crt.sh/?q={urllib.parse.quote('%.' + self.domain)}", headers=self.headers, timeout=timeout) as r:
                code = await r.text()
                for cert, domain in re.findall(
                        '<tr>(?:\s|\S)*?href="\?id=([0-9]+?)"(?:\s|\S)*?<td>([*_a-zA-Z0-9.-]+?\.' + re.escape(
                                self.domain) + ')</td>(?:\s|\S)*?</tr>', code, re.IGNORECASE):
                    domain = domain.split('@')[-1]
                    if domain not in self.domain_list:
                        self.domain_list.append(domain)
        except:
            info(f"crt.sh timeout! May need a larger timeout")
            return []
        info(f"crt.sh found {len(self.domain_list)} domains")
        return self.domain_list

    def print_domains(self, domain_list):
        if len(domain_list) > 1:
            for domain in domain_list:
                print(domain)


def main(url):
    certificate = Certificate(url)
    set = certificate.get_crtsh()

    task = asyncio.ensure_future(set)  # 异步执行函数
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print(task.result())


if __name__ == '__main__':
    main('hubu.edu.cn')
