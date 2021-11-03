#!/usr/bin/env python
"""
getdomain的主程序
"""
import sys
import argparse
from module.passive import search_engine, certificate
from module.active import csp_info
from lib.base import *
import asyncio
import json


# Check if we are running this on windows platform
is_windows = sys.platform.startswith('win')
# Console Colors
if is_windows:
    # Windows deserves coloring too :D
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white
    try:
        import win_unicode_console
        import colorama
        win_unicode_console.enable()
        colorama.init()
        # Now the unicode will work ^_^
    except:
        print("[!] Error: Coloring libraries not installed, no coloring will be used [Check the readme]")
        G = Y = B = R = W = G = Y = B = R = W = ''
else:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'   # white


# cancel color
def no_color():
    global G, Y, B, R, W
    G = Y = B = R = W = ''


def brand():
    print(f"""%s
           _         _ _                                   
 ___ _   _| |__   __| (_)___  ___ _____   _____ _ __ _   _ 
/ __| | | | '_ \ / _` | / __|/ __/ _ \ \ / / _ \ '__| | | |
\__ \ |_| | |_) | (_| | \__ \ (_| (_) \ V /  __/ |  | |_| |
|___/\__,_|_.__/ \__,_|_|___/\___\___/ \_/ \___|_|   \__, |
                                                     |___/ %sv1.0%s 
     you can use -h for help
     """ % (R, W, Y))


def cmd_line_parser():
    """
    This function parses the command line parameters and arguments
    """
    parser = argparse.ArgumentParser(usage="python " + sys.argv[0] + " [-h] [passive/active] -d [Domain] [Options]", epilog='\tExample: \r\npython ' + sys.argv[0] + " passive -d baidu.com -o html")
    parser._optionals.title = "OPTIONS"
    parser._positionals.title = "POSITION OPTIONS"

    parser.add_argument("scan_model", type=str, help="active or passive")

    # active part
    active = parser.add_argument_group("active", "active scan configuration options")
    active.add_argument("-x", "--xxxxx",  dest="load_config_file", default=False, action="store_true",
                        help="xxxxxxxxxxxx")

    # passive part
    passive = parser.add_argument_group("passive", "passive scan configuration options")
    passive.add_argument("-w", "--word-list", default=False, help="Custom brute force dictionary path")

    # other
    parser.add_argument("-d", "--domain", dest="domain", default=False, help="Target to scan")
    parser.add_argument("-m", "--multi-domain", dest="domains_file", default=False, help="Multi Target to scan")
    parser.add_argument("-o", "--format", default=False, help="The format of the output file")

    if len(sys.argv) == 1:
        sys.argv.append("-h")
    return parser.parse_args()


def main():
    """
    main function of getdomain

    python getdomain.py example.com -d word.txt
    :return:
    """
    brand()
    args = cmd_line_parser()
    domain = args.domain
    scan_model = args.scan_model
    loop = asyncio.get_event_loop()     # 获取事件循环
    tasks = []                          # 所有待处理的任务
    output_path = './data/output/results.json'    # 输出的json文件存放位置

    result = []

    if scan_model == "passive":
        se = search_engine.SearchEngine(domain)
        cer = certificate.Certificate(domain)
        tasks.append(asyncio.ensure_future(se.get_by_baidu()))  # 将任务加入任务列表 baidu搜索
        tasks.append(asyncio.ensure_future(se.get_by_bing()))   # bing搜索
        tasks.append(asyncio.ensure_future(cer.get_crtsh()))    # crt.sh搜索
        done, pending = loop.run_until_complete(asyncio.wait(tasks))    # 开始事件循环
        for task in tasks:
            # print(task.result())    # 获得结果
            result.extend(list(task.result()))

    elif scan_model == "active":
        set1 = set()
        tasks = []

        for i in ['http://', 'https://']:
            tasks.append(loop.create_task(csp_info.main(i + domain)))  # 使用create_task获取返回值
        loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            set1 = set1 | task.result()
        info(f"CSP found {len(set1)} domains")

    # 保存结果
    with open(output_path, 'w') as f:   # 保存json结果到./data/output/results.json
        json.dump({domain: list(set(result))}, f, indent=4, separators=(', ', ': '))

    info(f"All domains have been saved in {output_path}")
    info(f"Finish！！！！！")


if __name__ == '__main__':
    main()
