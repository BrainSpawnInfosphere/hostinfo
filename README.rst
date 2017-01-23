
hostinfo
=========

.. image:: https://api.codacy.com/project/badge/Grade/0e28e971366e4abfaf79c668d19d8356
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/kevin-walchko/hostinfo?utm_source=github.com&utm_medium=referral&utm_content=walchko/hostinfo&utm_campaign=badger

.. image:: https://raw.githubusercontent.com/walchko/hostinfo/master/pics/example.png
	:align: center



.. image:: https://travis-ci.org/walchko/hostinfo.svg?branch=master
    :target: https://travis-ci.org/walchko/hostinfo
	:alt: Travis-ci
.. image:: https://img.shields.io/pypi/v/hostinfo.svg
    :target: https://pypi.python.org/pypi/hostinfo/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/hostinfo.svg
    :target: https://pypi.python.org/pypi/hostinfo/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/l/hostinfo.svg
    :target: https://pypi.python.org/pypi/hostinfo/
    :alt: License


Install
--------

The preferred way is to use ``pip`` with `pypi.org <https://pypi.python.org/pypi>`_ ::

    pip install hostinfo

For development you can also do::

    git clone https://github.com/walchko/hostinfo.git
    cd hostinfo
    pip install -e .

Usage
------

Now in order to determine your ip and mac address, you need to supply an
interface. You can also supply a port to serve up the webpage. To speed up
things, generating a QR code is off by default.

::

	kevin@Logan hostinfo $ infoserver.py --help
	usage: infoserver.py [-h] [-v] [-e ETHERNET] [-p PORT] [-q]

	Launches a server that reports host information via a static web page. Example:

		infoserver.py -p 8800 -e en0 -q

	optional arguments:
	  -h, --help            show this help message and exit
	  -v, --version         show program's version number and exit
	  -e ETHERNET, --ethernet ETHERNET
	                        ethernet interface, default is eth0
	  -p PORT, --port PORT  port, default is 9000
	  -q, --qr              display a QR code of the host info

QR Reader
-------------

A sample view of a qr reader on my iPhone.

.. image:: https://github.com/walchko/hostinfo/blob/master/pics/qr_reader.png?raw=true
	:align: center
	:width: 300px

Raspbian [Debian Jessie] Service
-----------------------------------

Now you can create a service that will always start up when the computer boots::

	pi@bender hostinfo $ more /etc/systemd/system/hostinfo.service
	[Service]
	ExecStart=/usr/local/bin/infoserver.py -p 8080 -e eth0 -q
	Restart=always
	StandardOutput=syslog
	StandardError=syslog
	SyslogIdentifier=hostinfo
	User=pi
	Group=pi
	Environment=NODE_ENV=production

	[Install]
	WantedBy=multi-user.target

Change the port, ethernet interface, and desire to generate a QR code to your
liking. Once you create this file, you need to do::

	pi@bender hostinfo $ sudo systemctl enable hostinfo
	Created symlink from /etc/systemd/system/multi-user.target.wants/hostinfo.service to /etc/systemd/system/hostinfo.service.

	pi@bender hostinfo $ sudo service hostinfo start

	pi@bender hostinfo $ sudo service hostinfo status
	● hostinfo.service
	   Loaded: loaded (/etc/systemd/system/hostinfo.service; enabled)
	   Active: active (running) since Sun 2017-01-22 13:14:26 MST; 7s ago
	 Main PID: 28533 (infoserver.py)
	   CGroup: /system.slice/hostinfo.service
	           └─28533 /usr/bin/python /usr/local/bin/infoserver.py -p 8080 -e et...

	Jan 22 13:14:26 bender systemd[1]: Started hostinfo.service.

Now just launch a browser and connect to ``computer:port`` for example
``bender.local:8080`` because that is what I set it too above.

Changes
--------

=============  ========  ======
Date           Version   Notes
=============  ========  ======
22 Jan 17      0.2.1     bug fixes, working on macOS and Raspbian
21 Jan 17      0.1.0     init
=============  ========  ======

License
----------

**The MIT License (MIT)**

Copyright (c) 2017 Kevin J. Walchko

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
