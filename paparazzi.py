"""
Simple HTTP(S) screenshoter using Selenium and Chrome Driver.
"""

import os
import argparse
from pathlib import Path
from colorama import Fore
from selenium import webdriver
from multiprocessing import Pool

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
    parser.add_argument('input_file', help="List of hosts to screenshot")
    parser.add_argument('-o', '--output_dir', help="On which directory do you want to save screenshots?", default=None)
    parser.add_argument('-p', '--proxy', help="Do you want to use proxy? scheme://[user:password@]host:port", default=None)
    return parser.parse_args()

class Paparazzi(object):
    """A really disturbing person..."""
    def __init__(self, input_file, output_dir, proxy):
        self.input_file = input_file
        self.output_dir = output_dir
        self.proxy = proxy
        with open(self.input_file, 'r') as fd_in:
            self.hosts_list = [host.strip() for host in fd_in.readlines()]
        self.grapeshot()

    def grapeshot(self):
        """Let's go."""
        if self.output_dir and not Path(self.output_dir).exists():
            print_warning('{} does not exist, creating it...'.format(self.output_dir))
            try:
                access_rights = 0o755
                os.makedirs(self.output_dir, access_rights)
            except OSError:
                print_error('Error creating {}!')

        with Pool(os.cpu_count()) as pool:
            pool.map(self.screenshot, self.hosts_list)

    def screenshot(self, url):
        """Nice shot!"""
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            if self.proxy:
                options.add_argument('--proxy-server={}'.format(self.proxy))
            desired_caps = options.to_capabilities()
            desired_caps['acceptInsecureCerts'] = True

            driver = webdriver.Chrome(desired_capabilities=desired_caps)

            driver.get(url)
            if self.output_dir:
                output = '{}/{}.png'.format(self.output_dir, url.split('://')[1])
            else:
                output = '{}.png'.format(url.split('://')[1])
            driver.save_screenshot(output)
            driver.close()
            print_success('Screenshot of {} OK!'.format(url))
        except:
            print_error('Screenshot of {} KO...'.format(url))

if __name__ == '__main__':
    args = usage()
    print_info("Are you an annoying paparazzi?")
    if args.proxy:
        print_info('Using proxy: {}'.format(args.proxy))
    Paparazzi(args.input_file, args.output_dir, args.proxy)
