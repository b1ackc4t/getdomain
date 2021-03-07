#!/usr/bin/env python
import sys
import argparse


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

    parser.add_argument("scan-model",  type=str, help="active or passive")

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
    args = parser.parse_args()
    return args


def main():
    """
    main function of subDiscovery

    python subdiscovery.py example.com -d word.txt
    :return:
    """
    brand()
    args = cmd_line_parser()

    print(args)


if __name__ == '__main__':
    main()
