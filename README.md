Paparazzi
=========

Description
-----------
A really simple HTTP(S) screenshoter using Selenium and Chrome Driver.
I enjoyed a lot [webscreenshot](https://github.com/maaaaz/webscreenshot) but was bored
of empty screenshots produced when screenshoting HTTPS websites with a self-signed certificate.
As [maaaaz](https://github.com/maaaaz) explained, the reason is that the [`--ignore-certificate-errors`](https://groups.google.com/a/chromium.org/forum/#!topic/headless-dev/eiudRsYdc3A) option doesn't work and will never work anymore: the solution is to use a [proper webdriver](https://bugs.chromium.org/p/chromium/issues/detail?id=697721).

Requirements
--------
* Python 3
* [Selenium](https://www.seleniumhq.org/): `pip install -U selenium`
* [Chrome Driver](https://chromedriver.storage.googleapis.com/index.html?path=2.42/)
* Chrome Driver has to be in PATH...