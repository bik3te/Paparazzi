# Paparazzi

## Description

A really simple HTTP(S) screenshoter using Selenium and Chrome Driver.
I enjoyed a lot [webscreenshot](https://github.com/maaaaz/webscreenshot) but was bored
of empty screenshots produced when screenshoting HTTPS websites with a self-signed certificate.
As [maaaaz](https://github.com/maaaaz) explained, the reason is that the [`--ignore-certificate-errors`](https://groups.google.com/a/chromium.org/forum/#!topic/headless-dev/eiudRsYdc3A) option doesn't work and will never work anymore: the solution is to use a [proper webdriver](https://bugs.chromium.org/p/chromium/issues/detail?id=697721).

## Acknowledgments
This repository contains the great ERNW's [nmap-parse-output](https://github.com/ernw/nmap-parse-output) as submodule.

## Requirements

* Python 3
* [xsltproc](http://xmlsoft.org/XSLT/xsltproc.html)
* [Selenium](https://www.seleniumhq.org/): `pip install -U selenium`
* [Chrome Driver](https://chromedriver.storage.googleapis.com/index.html?path=2.42/) which has to be in PATH...

## Installation
```
$ git clone https://github.com/bik3te/Paparazzi --recurse-submodules
```
