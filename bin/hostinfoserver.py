#!/usr/bin/env python

from __future__ import print_function
from __future__ import division
from flask import Flask
from flask import render_template
import datetime as dt
import hostinfo
from hostinfo import HostInfo
from hostinfo import getOSImage
import pkg_resources
import argparse
# from hostinfo.qr_code import QRCode


def handleArgs():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description="""
Launches a server that reports host information via a static web page. Example:
	hostinfoserver.py -p 8800 -e en0 -q
""")
	parser.add_argument('-e', '--ethernet', help='ethernet interface, default is eth0', default='eth0')
	parser.add_argument('-p', '--port', help='port, default is 9000', type=int, default=5000)
	parser.add_argument('-i', '--ip', help='host ip address, default is 0.0.0.0', default='0.0.0.0')
	parser.add_argument('--version', action='version', version=hostinfo.__version__)
	# parser.add_argument('-q', '--qr', help='display a QR code of the host info', action='store_true')

	return vars(parser.parse_args())


def generator(en):
	"""
	This generates the webpage.
	"""
	ci = HostInfo(iface=en)
	data = ci.get()

	# QR = False
	# if QR:
	# 	png = None
	# 	if png is None:
	# 		qr = QRCode()
	# 		png = qr.create(data['data'])

	return data['data']


host_data = []  # generator(args['ethernet'])


app = Flask(
	'hostinfo',
	template_folder=pkg_resources.resource_filename('hostinfo', 'templates'),
	static_folder=pkg_resources.resource_filename('hostinfo', 'static')
)


@app.route('/')
def root():
	# regenerate data after a while
	if False:
		# time stamp
		global host_data
		host_data = generator()
	# print(data)
	now = dt.datetime.now()
	creation_time = now.ctime()
	os_name = ' '.join(host_data[1])
	return render_template(
		'main.html',
		items=host_data,
		time=creation_time,
		os_image=getOSImage(os_name)), 200


@app.route('/json')
def json_data():
	print('they want json!!')
	return 'hello', 200


@app.errorhandler(404)
def page_not_found(error):
	# app.logger.error('Page not found: %s', (request.path))
	return render_template('404.html'), 404


if __name__ == '__main__':

	args = handleArgs()

	# global host_data
	host_data = generator(args['ethernet'])

	app.run(host=args['ip'], port=int(args['port']))
