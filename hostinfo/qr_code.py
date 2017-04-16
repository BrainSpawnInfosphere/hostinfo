# import qrcode
#
# This is neat and all, but not necessary
#
#
# class QRCode(object):
# 	"""
# 	Given a computer's info, this will generate a QR image.
# 	"""
# 	template = [
# 		'Host: {host}',
# 		'OS: {os}',
# 		'IPv4: {ipv4}',
# 		'MAC: {mac}',
# 		'CPU: {cpu}',
# 		'Arch: {arch}',
# 		'RAM: {ram}'
# 	]
#
# 	def create(self, info):
# 		qr = qrcode.QRCode()
# 		txt = os.linesep.join(self.template)
# 		txt = txt.format(
# 			host=info[0][1],
# 			os=info[1][1],
# 			ipv4=info[8][1],
# 			mac=info[9][1],
# 			cpu=info[2][1],
# 			arch=info[3][1],
# 			ram=info[7][1].split(' / ')[1]
# 		)
# 		disks = []
# 		for i in info:
# 			if i[0].find('/') >= 0:
# 				disks.append(' '.join(i))
# 		txt = txt + '\n' + '\n'.join(disks)
# 		qr.add_data(txt)
# 		qr.make(fit=True)
# 		return qr.make_image()._repr_png_()
