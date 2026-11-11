# HoneyThing (Python 3)

Adapted from https://github.com/omererdem/honeything by Ömer Erdem (idea by Ali Ikinci, Honeynet GSoC 2015). The original runs only on Python 2.7; this copy is a Python 3 migration of its last commit (fe47ba9, March 2016) that keeps the honeypot's behaviour unchanged. Licence: GNU GPL v3 (see LICENSE); the embedded catawampus TR-069 code is Google's, under the Apache License 2.0 (src/cwmp/LICENSE).

## Changes for Python 3

- Converted with 2to3, then fixed by hand where 2to3 is not enough: relative imports in catawampus, bytes and text in the HTTP server, tornado's curl client, the Digest authentication helper (curtain), xmlwitch, the CWMP logger and the SOAP handler, the `iteritems` family on catawampus's own dictionary classes, and a `str`/`float` comparison in the download scheduler that Python 2 allowed.
- `src/cwmp/platform` is renamed `src/cwmp/cpe_platform`, because on Python 3 it hid the standard library's `platform` module (needed by `uuid`).
- `cgi` (removed in Python 3.13) is no longer used: form parsing uses `urllib.parse` and `email`.
- Responses stay byte-for-byte as under Python 2.7: the web server keeps Python 2's error page and header order (`send_error`), and HTTP headers on port 7547 and XML namespace attributes are emitted in Python 2.7 dict order (`src/cwmp/tr/vendor/py2order.py`). The CWMP process still names itself `cwmpd`.
- HoneyThing starts `cwmpd` with its own interpreter (`sys.executable`).
- Optional: the environment variable `HONEYTHING_CONFIG` sets the path of `config.ini` (default `/opt/honeything/config/config.ini`, as before).
- Tested with Python 3.11 and pycurl 7.49.0 on Debian 12, against the original running on Python 2.7.18: identical responses on ports 80 and 7547 and identical log formats (only the order of POST fields in `http.log` differs).

To run from a checkout: copy `src/config/config.ini` to `/opt/honeything/config/` (or set `HONEYTHING_CONFIG`), create the log, download, spool and run directories it names, `pip install pycurl`, then `PYTHONPATH=<checkout> python3 <checkout>/src/HoneyThing.py`. Set `acs_url` in `config.ini` to an ACS you control: the default, `http://IP:8080/libreacs/acs`, is a placeholder.

---

# HoneyThing
HoneyThing is a honeypot for Internet of TR-069 things. It's designed to act as completely a modem/router that has RomPager embedded web server and supports [TR-069 (CWMP)](https://www.broadband-forum.org/technical/download/TR-069_Amendment-5.pdf) protocol.

Project idea was created by [Ali Ikinci](https://github.com/aikinci) and offered as [Honeynet GSoC](https://honeynet.org/gsoc/ideas#project15) project in 2015.

## Features
Basic features:

 - Emulates some popular vulnerabilities for RomPager as [Misfortune Cookie](http://mis.fortunecook.ie/), [Rom-0](https://ripe69.ripe.net/presentations/61-rom0-vuln.pdf) etc.
 - TR-069 protocol support. Implements mostly used TR-069 CPE commands. e.g: GetRPCMethods, Get/Set ParameterValues, Download...
 - Modem web interface to increase the interaction with attacker.
 - All communication with services (http.log, cwmp.log) and state of honeypot (started/stopped, error etc. to honeything.log) are logged in parsable text format.
 
## Download
Debian and RPM packages will be available soon.

## Installation
There're 2 ways to install HoneyThing:

For all of them, your system must have Python 2.7 (or above) and [PycURL](https://pypi.python.org/pypi/pycurl) package.

 - **Setup Script:** Using setup script requires [python setuptools](https://pypi.python.org/pypi/setuptools) package installed on the system. After downloading and extracting HoneyThing, you can simply go to extracted directory and run; 
> python setup.py install

 - **Pre-Built Packages:** HoneyThing can be installed by using pre-built packages for Ubuntu and CentOS. Packages can be downloaded from [download section](#download) and will be added for any stable release.
 
 For Ubuntu;
> dpkg -i honeything_x.y.z.deb
 
 For CentOS;
> rpm -i honeything_x.y.z.rpm

## Configuration
After installation, some parameters can be changed optional by using [configuration file](https://github.com/omererdem/honeything/blob/master/src/config/config.ini). There're 4 section in config file:

 - **http:** HTTP listen address/port can be edited in this section.
 - **cwmp:** Some TR-069 parameters as listen address/port, ACS url, download directory for *"download"* CPE command, connection request path etc. can be edited.
 - **cpe:** In cpe section, there're lots of variables related to modem/router device like manufacturer, serial number, model name etc. They can be edited to provide device variety in ACS communication.
 - **logging:** Log file paths, log level and some protocol specific parameters can be changed in this section.

## Run
If you installed HoneyThing with setup script or pre-built packages, honeything can be run by using following commands:

> service honeything {start|stop|restart|status}

or
> /etc/init.d/honeything {start|stop|restart|status}

## Documentation
A paper about this project is published (in TURKISH) at International Conference on Information Security and Cryptology [[ISCTurkey 2015]](http://www.iscturkey.org/en). It is accessible online from [here](http://www.iscturkey.org/s/2226/i/HoneyThing_Revised_Last.pdf).

## Credits
The project:

 - Developed by [Ömer Erdem](https://github.com/omererdem)
 - Idea by [Ali Ikinci](https://github.com/aikinci)
 - Advisor [Dr. Mehmet Kara](https://tr.linkedin.com/in/mehmet-kara-b2335947)

and special thanks to [Bâkır Emre](https://github.com/bemre) for taking the first step.


**Note:** This project is also being developed as Istanbul Sehir University master's thesis.
