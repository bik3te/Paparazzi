"""
Simple HTTP(S) screenshoter using Selenium and Chrome Driver.
"""

import io
import os
import time
import shlex
from pathlib import Path
from selenium import webdriver
from subprocess import run, PIPE
from multiprocessing.dummy import Pool as ThreadPool
from utils.funcs import usage, print_info, print_warning, print_error, print_success

class Paparazzi(object):
    """A really disturbing person..."""
    def __init__(self, input_file, output_dir, nb_threads, proxy):
        self.input_file = input_file
        self.output_dir = output_dir
        self.nb_threads = nb_threads
        self.proxy = proxy
        self.hosts_list = [host.strip().decode('utf-8') for host in self.hosts_gen()]
        self.grapeshot()

    def hosts_gen(self):
        """Parse Nmap XML and look for hosts with HTTP(S) services."""
        command = './utils/nmap-parse-output/nmap-parse-output {} http-ports'.format(self.input_file)
        res = run(shlex.split(command), stdout=PIPE)
        return io.BytesIO(res.stdout).readlines()

    def grapeshot(self):
        """Let's go."""
        if not Path(self.output_dir).exists():
            print_warning('{} does not exist, creating it...'.format(self.output_dir))
            try:
                access_rights = 0o755
                os.makedirs(self.output_dir, access_rights)
            except OSError:
                print_error('Error creating {}!')

        with ThreadPool(self.nb_threads) as pool:
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
            output = '{}/{}.png'.format(self.output_dir, url.split('://')[1])
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
    start_time = time.time()
    Paparazzi(args.input_file, args.output_dir, args.threads, args.proxy)
    print_success('Grapeshotted in {} seconds.'.format(time.time() - start_time))
