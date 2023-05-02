"""
Simple HTTP(S) screenshoter using Selenium and Chrome Driver.
"""

import io
import sys
import time
import json
import shlex
import socket
from subprocess import run, PIPE
from shutil import copytree
from multiprocessing.dummy import Pool as ThreadPool

from selenium import webdriver
from selenium.webdriver.common.by import By
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
        self.interface_types = {
            'Tomcat': 'Apache Tomcat',
            'Jenkins': 'Jenkins',
            'Hudson': 'Hudson',
            'Jira': 'Atlassian Jira'
        }
        self.found_interfaces = {
            'Tomcat': [],
            'Jenkins': [],
            'Hudson': [],
            'Jira': [],
            'Undefined': []
        }
        self.hosts_list = []
        self.screenshots = []
        self.grapeshot()
        self.create_gallery()
        self.save_discovery()

    def hosts_gen(self):
        """Parse Nmap XML and look for hosts with HTTP(S) services."""
        command = './utils/nmap-parse-output/nmap-parse-output {} http-ports'.format(self.input_file)
        res = run(shlex.split(command), stdout=PIPE)
        return io.BytesIO(res.stdout).readlines()

    def hosts_file(self, hosts_input):
        """Take a host file as input."""
        with open(hosts_input, 'r') as fd_in:
            hosts = fd_in.readlines()
        return [host.strip() for host in hosts]

    def grapeshot(self):
        """Let's go."""
        try:
            copytree('data', self.output_dir)
        except:
            print_error('Error creating {}, directory exist!'.format(self.output_dir))
            sys.exit(1)
        with open(self.input_file, 'r') as fd_in:
            data = fd_in.readline()

        if data == '<?xml version="1.0" encoding="UTF-8"?>\n':
            self.hosts_list = [host.strip().decode('utf-8') for host in self.hosts_gen()]
        else:
            self.hosts_list = self.hosts_file(self.input_file)
        print_info('{} hosts to screenshot!'.format(len(self.hosts_list)))

        with ThreadPool(self.nb_threads) as pool:
            pool.map(self.screenshot, self.hosts_list)

    def screenshot(self, url):
        """Nice shot!"""
        # Host is up and not filtered?
        timeout = False
        socket.setdefaulttimeout(3)
        host, port = (url.split('://')[1].split(':')[0], url.split('://')[1].split(':')[1])
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((host, int(port)))
            except:
                print_error('Screenshot of {} KO! Host is down or communication is filtered...'.format(url))
                timeout = True

        if not timeout:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            if self.proxy:
                options.add_argument('--proxy-server={}'.format(self.proxy))
            desired_caps = options.to_capabilities()
            desired_caps['acceptInsecureCerts'] = True

            driver = webdriver.Chrome(options=options, desired_capabilities=desired_caps)

            # Content is not bullshit?
            try:
                interface_found = False
                driver.get(url)
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'title'))
                )
                title = driver.title
                output = '{}/images/{}.png'.format(self.output_dir, url.split('://')[1])
                driver.save_screenshot(output)

                for interface in self.interface_types:
                    if self.interface_types[interface].lower() in driver.page_source.lower():
                        self.found_interfaces[interface] += [url]
                        interface_found = True
                        print_success('Screenshot of {} OK! -> {} interface'.format(url, interface))

                if not interface_found:
                    self.found_interfaces['Undefined'] += [url]
                    print_success('Screenshot of {} OK!'.format(url))

                self.screenshots.append({'url': url, 'path': output.replace('{}/'.format(self.output_dir), ''), 'title': title})
                driver.close()
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

    def save_discovery(self):
        """Logging sensitive interfaces."""
        print_info('Storing sensitive interfaces into {}/interfaces.json...'.format(self.output_dir))
        with open('{}/interfaces.json'.format(self.output_dir), 'w') as fd_out:
            fd_out.write(json.dumps(self.found_interfaces))

if __name__ == '__main__':
    args = usage()
    print_info("Are you an annoying paparazzi?")
    if args.proxy:
        print_info('Using proxy: {}'.format(args.proxy))
    start_time = time.time()
    Paparazzi(args.input_file, args.output_dir, args.threads, args.proxy)
    print_success('Grapeshotted in {} seconds.'.format(time.time() - start_time))
