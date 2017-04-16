from __future__ import print_function
from __future__ import division
import platform         # gets host info
import psutil as ps     # gets host info
import datetime as dt
# import socket
import cpuinfo

from platform import python_version
import subprocess
# from build_utils import python_version


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
		ret = ('apple', '#555555')
	elif distro.find('debian') >= 0:
		ret = ('debian', 'red')
	elif distro.find('redhat') >= 0:
		ret = ('redhat', 'red')
	elif distro.find('slackware') >= 0:
		ret = ('slackware', 'SLATEBLUE')
	elif distro.find('gentoo') >= 0:
		ret = ('gentoo', 'PLUM')
	elif distro.find('suse') >= 0:
		ret = ('opensuse', 'green')
	elif distro.find('centos') >= 0:
		ret = ('centos', 'purple')
	elif distro.find('ubuntu') >= 0:
		ret = ('ubuntu', 'orangered')
	elif distro.find('fedora') >= 0:
		ret = ('fedora', 'blue')
	else:
		ret = ('linux', 'black')

	return ret


if python_version().split('.')[0] == '2':
	def getoutput(cmd):
		return subprocess.check_output([cmd], shell=True)
else:
	def getoutput(cmd):
		return subprocess.getoutput(cmd)


class HostInfo(object):
	"""
	This collects info on a host computer and generates a dictionary
	of it.
	"""
	TB = 2**40
	GB = 2**30
	MB = 2**20
	KB = 2**10

	def __init__(self, iface='en0'):
		self.iface = iface
		self.system = platform.system()
		self.info = cpuinfo.get_cpu_info()
		self.macaddr = None

	def get(self):
		info = [
			['host', platform.node()],
			[self.os(), self.release()],
			['CPU:', self.cpu()],
			['Arch:', self.arch()],
			['Load:', self.load()],
			['Compiler:', platform.python_compiler()],
			['Python:', platform.python_version()],
			['Memory:', self.ram()],
			['IPv4:', self.ipv4()],
			['IPv6:', self.ipv6()],
			['MAC:', self.mac()],
			['Uptime:', self.uptime()],
			['Processes:', str(len(ps.pids())) + ' running'],
			['Packages', self.packages()]
		]
		disks = self.disks()
		for d in disks:
			info.append(d)

		return {'data': info}

	def release(self):
		if self.system == 'Darwin':
			s = platform.mac_ver()
			rel = s[0]
		elif self.system == 'Linux':
			s = platform.linux_distribution()
			rel = '{} {}'.format(s[0], s[1])
		return rel

	def uptime(self):
		# fix me!!
		up = ps.boot_time()
		up = dt.datetime.fromtimestamp(up)
		now = dt.datetime.now()
		diff = now - up
		uptime = '{} days {} hrs {} mins'.format(diff.days, diff.seconds // 3600, (diff.seconds % 3600) // 60)
		return uptime

	def disks(self):
		disks = ps.disk_partitions()
		ret = []
		for d in disks:
			# if d.mountpoint == '/dev/mmcblk0p1':
			# 	continue
			p = ps.disk_usage(d.mountpoint)
			# if d.fstype != 'vfat':
			# ret.append([d.device, '{} {} / {} GB'.format(d.fstype, p.used // self.GB, p.total // self.GB)])
			if p.total > self.TB:
				ret.append([d.mountpoint, '{} {} / {} TB'.format(d.fstype, p.used // self.TB, p.total // self.TB)])
			elif p.total > self.GB:
				ret.append([d.mountpoint, '{} {} / {} GB'.format(d.fstype, p.used // self.GB, p.total // self.GB)])
			elif p.total > self.MB:
				ret.append([d.mountpoint, '{} {} / {} MB'.format(d.fstype, p.used // self.MB, p.total // self.MB)])
			else:
				ret.append([d.mountpoint, '{} {} / {} B'.format(d.fstype, p.used, p.total)])
		return ret

	def ram(self):
		ram = ps.virtual_memory()
		used = ram.used
		total = ram.total
		if total > self.GB:
			used = used // self.GB
			total = total // self.GB
			s = '{} / {} GB'.format(used, total)
		else:
			used = used // self.MB
			total = total // self.MB
			s = '{} / {} MB'.format(used, total)
		return s

	def mac(self):
		if self.macaddr is None:
			if self.system == 'Darwin':
				self.macaddr = getoutput("ifconfig " + self.iface + "| grep ether | awk '{ print $2 }'")
			else:
				self.macaddr = getoutput("ifconfig " + self.iface + "| grep HWaddr | awk '{ print $5 }'")

		return self.macaddr

	def ipv4(self):
		if self.system == 'Darwin':
			ipv4 = getoutput("ifconfig " + self.iface + " | grep 'inet ' | awk '{ print $2 }'")
		else:
			ipv4 = getoutput("ifconfig " + self.iface + " | grep 'inet addr' | awk '{ print $2 }'")
			ipv4 = ipv4.split(':')[1]

		# ipv4 = socket.gethostbyname(platform.node())
		# if ipv4.split('.')[0] == '127':
		# 	ipv4 = socket.gethostbyname(platform.node() + '.local')
		return ipv4

	def ipv6(self):
		if self.system == 'Darwin':
			ipv6 = getoutput("ifconfig " + self.iface + "| grep inet6 | awk '{ print $2 }'")
		else:
			ipv6 = getoutput("ifconfig " + self.iface + "| grep inet6 | awk '{ print $3 }'")
		# result = socket.getaddrinfo(host, port, socket.AF_INET6)
		# return result[0][4][0]
		return ipv6

	def load(self):
		return str(ps.cpu_percent(interval=1, percpu=True))

	def os(self):
		sys = self.system
		if sys == 'Darwin':
			sys = 'macOS'
		return sys + ':'

	def cpu(self):
		ret = self.info['brand']
		if ret.find('@') < 0:
			ret = ret + ' @ ' + self.info['hz_actual']
		return ret

	def arch(self):
		ret = self.info['arch']
		return ret

	def packages(self):
		if self.system == 'Darwin':
			pkgs = getoutput('brew list').split('\n')
			ret = 'brew {} installed'.format(len(pkgs))
		elif self.system == 'Linux':
			pkgs = getoutput('dpkg -l').split('\n')
			ret = 'apt-get {} installed'.format(len(pkgs))
		return ret
