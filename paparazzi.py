"""
Simple HTTP(S) screenshoter using Selenium and Chrome Driver.
"""

import io
import sys
import time
import shlex
import socket
from subprocess import run, PIPE
from shutil import copytree, Error
from multiprocessing.dummy import Pool as ThreadPool

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils.funcs import usage, print_info, print_error, print_warning, print_success


class Paparazzi(object):
    """A really disturbing person..."""
    def __init__(self, input_file, output_dir, nb_threads, proxy):
        self.input_file = input_file
        self.output_dir = output_dir
        self.nb_threads = nb_threads
        self.proxy = proxy
        self.hosts_list = []
        self.screenshots = []
        self.cpt = 0
        self.grapeshot()
        self.create_gallery()

    def hosts_gen(self):
        """Parse Nmap XML and look for hosts with HTTP(S) services."""
        command = './utils/nmap-parse-output/nmap-parse-output {} http-ports'.format(self.input_file)
        res = run(shlex.split(command), stdout=PIPE)
        return io.BytesIO(res.stdout).readlines()

    def grapeshot(self):
        """Let's go."""
        try:
            copytree('data', self.output_dir)
        except:
            print_error('Error creating {}, directory exist!'.format(self.output_dir))
            sys.exit(1)
        self.hosts_list = [host.strip().decode('utf-8') for host in self.hosts_gen()]
        print_info('{} hosts to screenshot!'.format(len(self.hosts_list)))

        with ThreadPool(self.nb_threads) as pool:
            pool.map(self.screenshot, self.hosts_list)

    def screenshot(self, url):
        """Nice shot!"""
        # Host is up and not filtered?
        socket.setdefaulttimeout(3)
        host, port = (url.split('://')[1].split(':')[0], url.split('://')[1].split(':')[1])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, int(port)))
            except:
                print_error('Screenshot of {} KO! Host is down or communication is filtered...'.format(url))

        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        if self.proxy:
            options.add_argument('--proxy-server={}'.format(self.proxy))
        desired_caps = options.to_capabilities()
        desired_caps['acceptInsecureCerts'] = True

        driver = webdriver.Chrome(desired_capabilities=desired_caps)

        # Content is not bullshit?
        try:
            driver.get(url)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'title'))
            )
            title = driver.title
            output = '{}/images/{}.png'.format(self.output_dir, url.split('://')[1])
            driver.save_screenshot(output)
            driver.close()
            print_success('Screenshot of {} OK!'.format(url))
            self.screenshots.append({'url': url, 'path': output.replace('{}/'.format(self.output_dir), ''), 'title': title})
        except:
            print_warning('Did not took screenshot of {}! Bullshit or empty page...'.format(url))

    def sort_screenshots(self):
        """Sort screenshots by title."""
        self.screenshots = sorted(self.screenshots, key=lambda k: k['title'])

    def create_gallery(self):
        """Preparing the screenshot gallery!"""
        with open('data/index.html', 'r') as fd_in:
            template = fd_in.read()

        data = ''
        self.sort_screenshots()
        for screenshot in self.screenshots:
            data += """<div class="col-sm-6 col-md-4">
                          <div class="thumbnail">
                              <a class="lightbox" href="{}">
                                  <img src="{}" alt="{}">
                              </a>
                              <div class="caption">
                                  <h3>{}</h3>
                                  <p>{}</p>
                              </div>
                          </div>
                      </div>
                      """.format(screenshot['url'],
                                 screenshot['path'],
                                 screenshot['title'],
                                 screenshot['title'],
                                 screenshot['url'])

        with open('{}/index.html'.format(self.output_dir), 'w') as fd_out:
            fd_out.write(template.replace('[w00t]', data))

if __name__ == '__main__':
    args = usage()
    print_info("Are you an annoying paparazzi?")
    if args.proxy:
        print_info('Using proxy: {}'.format(args.proxy))
    start_time = time.time()
    Paparazzi(args.nmap_xml, args.output_dir, args.threads, args.proxy)
    print_success('Grapeshotted in {} seconds.'.format(time.time() - start_time))
