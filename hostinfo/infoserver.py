#!/usr/bin/env python

# for the webserver
from __future__ import print_function
from __future__ import division
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from simplehtml import HTML
import qrcode
import platform
from hostinfo import HostInfo
import hostinfo
import argparse
import os


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
	margin: 0 40px;
	text-decoration: none;
	color: #ffffff;
	text-transform: uppercase;
	font-size: 12px;
}
p {
	text-align: center;
}
"""

# I don't like globals, but this was a quick hack
png = None
QR = False
ETHER = None


class QRCode(object):
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
		qr.add_data(txt)
		qr.make(fit=True)
		return qr.make_image()._repr_png_()


def generator():
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
	html.linuxFont()

	html.css(css)

	sys = platform.system()
	if sys == 'Darwin':
		html.p('<i class="fl-apple fl-72" style="color: #555555"></i>')
	elif sys == 'Linux':
		s = platform.linux_distribution()
		if s[0] == 'debian':
			html.p('<i class="fl-debian fl-72" style="color: red"></i>')
		else:
			html.p('<i class="fl-linux fl-72" style="color: black"></i>')

	host = data['data'].pop(0)
	html.h1(host[1])
	html.table(data)

	if QR:
		html.img('qr.png', width='300px')

	html.footer('<a href="http://github.com/walchko/hostinfo"><i class="fl-github fl-24"></i></a>')

	return html


class GetHandler(BaseHTTPRequestHandler):

	def do_GET(self):
		if self.path == '/':
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			html = generator()

			self.wfile.write(html)

		elif self.path.rfind('.png') > 1:
			self.send_response(200)
			self.send_header('Content-type', 'image/png')
			self.end_headers()

			if self.path == '/qr.png':

				global QR
				if QR:
					global png
					if png:
						self.wfile.write(png)
			else:
				fname = self.path[1:]
				fd = open('./'+fname)
				im = fd.read()
				fd.close()
				self.wfile.write(im)

		else:
			self.send_response(404)
			self.send_header('Content-type', 'text/html')
			self.end_headers()

			html = HTML()
			html.css('h1 {text-align: center;}')
			html.css('p {text-align: center;}')
			html.h1('404')
			html.p('File not found: ' + self.path)

			self.wfile.write(str(html))


def handleArgs():
	parser = argparse.ArgumentParser(version=hostinfo.__version__, formatter_class=argparse.RawDescriptionHelpFormatter,
	description="""
Launches a server that reports host information via a static web page.
""")

	parser.add_argument('-e', '--ethernet', help='ethernet interface, default is ether0', default='ether0')
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
