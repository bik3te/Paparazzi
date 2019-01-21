"""
Paparazzi's utility functions.
"""

import argparse
from colorama import Fore

def print_success(message):
    print('{} [*] {}{}'.format(Fore.GREEN, message, Fore.RESET))

def print_error(message):
    print('{} [-] {}{}'.format(Fore.RED, message, Fore.RESET))

def print_info(message):
    print('{} [!] {}{}'.format(Fore.CYAN, message, Fore.RESET))

def print_warning(message):
    print('{} [!] {}{}'.format(Fore.YELLOW, message, Fore.RESET))

def usage():
    """Argument parser function."""
    parser = argparse.ArgumentParser(description="Please don't visit each page manually...")
    parser.add_argument('input_file', help="Nmap XML output file or hosts list (http[s]://<host>:<port>)")
    parser.add_argument('-o', '--output_dir', help="On which directory do you want your screenshot gallery? (default=./gallery)", default='./gallery')
    parser.add_argument('-p', '--proxy', help="Do you want to use proxy? scheme://[user:password@]host:port", default=None)
    parser.add_argument('-t', '--threads', help="How many threads to use? (default=8)", type=int, default=8)
    return parser.parse_args()
