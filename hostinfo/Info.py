
from __future__ import print_function
from __future__ import division
import commands         # get mac and ip addr
import platform         # gets host info
import psutil as ps     # gets host info
import datetime as dt
import socket
import cpuinfo


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
				self.macaddr = commands.getoutput("ifconfig " + self.iface + "| grep ether | awk '{ print $2 }'")
			else:
				self.macaddr = commands.getoutput("ifconfig " + self.iface + "| grep HWaddr | awk '{ print $5 }'")

		return self.macaddr

	def ipv4(self):
		ipv4 = socket.gethostbyname(platform.node())
		if ipv4.split('.')[0] == '127':
			ipv4 = socket.gethostbyname(platform.node() + '.local')
		return ipv4

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
		ret = ''
		if self.system == 'Darwin':
			pkgs = commands.getoutput('brew list').split('\n')
			ret = 'brew {} installed'.format(len(pkgs))
		elif self.system == 'Linux':
			pkgs = commands.getoutput('dpkg -l').split('\n')
			ret = 'apt-get {} installed'.format(len(pkgs))
		return ret
