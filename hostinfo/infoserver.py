#!/usr/bin/env python

# for the webserver
from __future__ import print_function
from __future__ import division
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from simplehtml import HTML
import qrcode
from hostinfo import HostInfo
import hostinfo
import argparse
import os
import datetime as dt
import pkg_resources


# The CSS for the webpage
css = """
h1 {
	text-align: center;
}
img {
	display: block;
	margin: 0 auto;
}
table {
	font-family: arial, sans-serif;
	border-collapse: collapse;
	width: 70%;
	margin-left: 15%;
	margin-right: 15%;
}
table tr td:first-child {
	text-align: right;
	font-weight: bold;
	padding-right: 10px;
}
footer {
	width: 100%;
	height: 44px;
	line-height: 44px;
	text-align: center;
	background-color: #888888;
	margin: 0px;
	padding: 0px;
	margin-top: 20px; /* space between content and footer */
	border-top: 5px solid #666666;
}
a {
	display: inline-block;
	# margin: 0 40px;
	text-decoration: none;
	color: #ffffff;
	# text-transform: uppercase;
	# font-size: 12px;
	text-align: center;
}
p {
	text-align: center;
}
.stamp {
	position: absolute;
	top: 0px;
	right: 10px;
	color: #ffffff;
}
.container {
	position: relative;
}
"""

# I don't like globals, but this was a quick hack
png = None
QR = False
ETHER = None


class QRCode(object):
	"""
	Given a computer's info, this will generate a QR image.
	"""
	template = [
		'Host: {host}',
		'OS: {os}',
		'IPv4: {ipv4}',
		'MAC: {mac}',
		'CPU: {cpu}',
		'Arch: {arch}',
		'RAM: {ram}'
	]

	def create(self, info):
		qr = qrcode.QRCode()
		txt = os.linesep.join(self.template)
		txt = txt.format(
			host=info[0][1],
			os=info[1][1],
			ipv4=info[8][1],
			mac=info[9][1],
			cpu=info[2][1],
			arch=info[3][1],
			ram=info[7][1].split(' / ')[1]
		)
		disks = []
		for i in info:
			if i[0].find('/') >= 0:
				disks.append(' '.join(i))
		txt = txt + '\n' + '\n'.join(disks)
		qr.add_data(txt)
		qr.make(fit=True)
		return qr.make_image()._repr_png_()


def getOSImage(distro):
	"""
	Looking at the output of platform.linux_distribution or platform.mac_ver, this
	returns the correct font-linux icon.
	
	linux_distribution(distname='', version='', id='', supported_dists=('SuSE',
	'debian', 'fedora', 'redhat', 'centos', 'mandrake', 'mandriva', 'rocks',
	'slackware', 'yellowdog', 'gentoo', 'UnitedLinux', 'turbolinux', 'Ubuntu'),
	full_distribution_name=1)
	"""
	distro = distro.lower()
	ret = ' '
	if distro.find('macos') >= 0 or distro.find('darwin') >= 0:
		ret = '<i class="fl-apple fl-72" style="color: #555555"></i>'
	elif distro.find('debian') >= 0:
		ret = '<i class="fl-debian fl-72" style="color: red"></i>'
	elif distro.find('redhat') >= 0:
		ret = '<i class="fl-redhat fl-72" style="color: red"></i>'
	elif distro.find('slackware') >= 0:
		ret = '<i class="fl-slackware fl-72" style="color: SLATEBLUE"></i>'
	elif distro.find('gentoo') >= 0:
		ret = '<i class="fl-gentoo fl-72" style="color: PLUM"></i>'
	elif distro.find('suse') >= 0:
		ret = '<i class="fl-opensuse fl-72" style="color: green"></i>'
	elif distro.find('centos') >= 0:
		ret = '<i class="fl-centos fl-72" style="color: PURPLE"></i>'
	elif distro.find('ubuntu') >= 0:
		ret = '<i class="fl-ubuntu fl-72" style="color: ORANGERED"></i>'
	elif distro.find('fedora') >= 0:
		ret = '<i class="fl-fedora fl-72" style="color: blue"></i>'
	else:
		ret = '<i class="fl-linux fl-72" style="color: black"></i>'

	return ret


def generator():
	"""
	This generates the webpage.
	"""
	global ETHER
	ci = HostInfo(iface=ETHER)
	data = ci.get()

	global QR
	if QR:
		global png
		if png is None:
			qr = QRCode()
			png = qr.create(data['data'])

	html = HTML()
	html.cssLink('font-linux.css')

	html.css(css)

	os_name = ' '.join(data['data'][1])
	html.p(getOSImage(os_name))

	host = data['data'].pop(0)
	html.h1(host[1])
	html.table(data)

	if QR:
		html.img('qr.png', width='300px')

	now = dt.datetime.now()
	html.footer('<div class="container"><a href="http://github.com/walchko/hostinfo"><i class="fl-github fl-24"></i></a> <div class="stamp">{}</div></div>'.format(now.ctime()))

	return html


class GetHandler(BaseHTTPRequestHandler):
	# http://stackoverflow.com/questions/40867447/python-simple-http-server-not-loading-font-awesome-fonts
	def do_GET(self):
		global png

		print('path >> ', self.path)
		if self.path == '/':
			self.path = 'index.html'

		try:
			ext = self.path.split('.')[1]
			mimetype = {
				'html': 'text/html',
				'css':  'text/css',
				'woff': 'application/font-woff',
				'ttf':  'application/x-font-ttf',
				'eot':  'application/vnd.ms-fontobject',
				'svg':  'image/svg+xml',
				'png':  'image/png'
			}

			self.send_response(200)
			self.send_header('Content-type', mimetype[ext])
			self.end_headers()

			if ext == 'png':
				self.wfile.write(png)
			elif ext == 'html':
				html = generator()
				self.wfile.write(html)
			else:
				DATA_PATH = pkg_resources.resource_filename('hostinfo', 'assets/font-linux.' + ext)
				im = open(DATA_PATH).read()
				self.wfile.write(im)

		except (IOError, IndexError, KeyError):
			print('404 >> ', self.path)
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			html = HTML()
			html.css('h1 {text-align: center;}')
			html.css('p {text-align: center;}')
			html.h1('404')
			html.p('File not found: ' + self.path)

			self.wfile.write(html)


def handleArgs():
	parser = argparse.ArgumentParser(version=hostinfo.__version__, formatter_class=argparse.RawDescriptionHelpFormatter,
	description="""
Launches a server that reports host information via a static web page. Example:

	infoserver.py -p 8800 -e en0 -q
""")

	parser.add_argument('-e', '--ethernet', help='ethernet interface, default is eth0', default='eth0')
	parser.add_argument('-p', '--port', help='port, default is 9000', type=int, default=9000)
	parser.add_argument('-q', '--qr', help='display a QR code of the host info', action='store_true')

	args = vars(parser.parse_args())

	return args


if __name__ == '__main__':
	args = handleArgs()
	if args['qr']:
		QR = True
	ETHER = args['ethernet']
	port = args['port']
	print ('Starting server on port: ' + str(port) + ', use <Ctrl-C> to stop')
	server = HTTPServer(('0.0.0.0', port), GetHandler)
	server.serve_forever()
	
	print('Good bye')
