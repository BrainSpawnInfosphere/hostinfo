#!/usr/bin/env python

# for the webserver
from __future__ import print_function
from __future__ import division
from BaseHTTPServer import HTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
# from socket import gethostname, gethostbyname
from simplehtml import HTML
import qrcode
import platform
from hostinfo import HostInfo


PORT = 8800
png = None


def generator():
	ci = HostInfo()
	data = ci.get()

	global png
	qr = qrcode.QRCode()
	qr.add_data(str(data['data']))
	qr.make(fit=True)
	img = qr.make_image()
	# img.save('qr.png')
	png = img._repr_png_()

	html = HTML()
	html.linuxFont()

	html.css("""
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
	# background-color: #e0e0e0;
	text-align: right;
	font-weight: bold;
	padding-right: 10px;
}
# td, th {
# 	border: 1px solid #dddddd;
# 	text-align: left;
# 	padding: 8px;
# }
# tr:nth-child(even) {
# 	background-color: #dddddd;
# }
footer {
	# position: fixed;
	# bottom: 0px;
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
	# color: #555555;
}
	""")

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


if __name__ == '__main__':
	print ('Starting server ' + ':' + str(PORT) + ', use <Ctrl-C> to stop')
	server = HTTPServer(('0.0.0.0', PORT), GetHandler)
	server.serve_forever()
