import re
import requests



def match_subdomains(domain,subdomians,resp):
    '''
    匹配子域名
    '''
    result = re.findall(r'(?:[a-z0-9](?:[a-z0-9\-]{0,61}[a-z0-9])?\.){0,}' \
                        + domain.replace('.', r'\.'), resp, re.I)
    for subdoamin in result:
        subdoamin = subdoamin.split('@')[-1]
        if not subdoamin in subdomians:
            subdomians.append(subdoamin)
    return subdomians



# def get_subdomains(url,domain,subdomains):
#     resp = requests.get(url).text
#     subdomians = match_subdomains(domain, subdomains, resp.text)
#     return subdomians