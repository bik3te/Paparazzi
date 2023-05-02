# Paparazzi

## Description

A really simple HTTP(S) screenshoter using Selenium and Chrome Driver.
I enjoyed a lot [webscreenshot](https://github.com/maaaaz/webscreenshot) but was bored
of empty screenshots produced when screenshoting HTTPS websites with a self-signed certificate.
As [maaaaz](https://github.com/maaaaz) explained, the reason is that the [`--ignore-certificate-errors`](https://groups.google.com/a/chromium.org/forum/#!topic/headless-dev/eiudRsYdc3A) option doesn't work and will never work anymore: the solution is to use a [proper webdriver](https://bugs.chromium.org/p/chromium/issues/detail?id=697721).

It supports proxy - http or socks. It is multi-threaded and double-check if the service is down or the communication is filtered and doesn't take screenshots of empty pages or pages with useless text content.

A host to screenshot list - protocol://ip_or_hostname:port - or an XML nmap output has to be given as input to Paparazzi.

The results can be reviewed thanks to a simple bootstrap gallery, ordered by HTML titles - so likely interface types...

Finally, a JSON structure mapping hosts with interface types will also be part of the output. It is based on keywords matching and has to be completed - work-in-progress... This structure will be used as input for a future default password bruteforce script.

## Acknowledgments
This repository contains the great ERNW's [nmap-parse-output](https://github.com/ernw/nmap-parse-output) as submodule.

## Requirements

* Python 3
* [xsltproc](http://xmlsoft.org/XSLT/xsltproc.html)
* [Selenium](https://www.seleniumhq.org/): `pip install -U selenium`
* [colorama](https://pypi.org/project/colorama/): `pip install -U colorama`
* [Chrome Driver](https://chromedriver.chromium.org/downloads) which has to be in PATH...

## Installation
```
$ git clone https://github.com/bik3te/Paparazzi --recurse-submodules
```
