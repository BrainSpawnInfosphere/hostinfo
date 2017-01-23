import os
from setuptools import setup
from setuptools.command.test import test as TestCommand
from hostinfo import __version__ as VERSION


class PublishCommand(TestCommand):
	def run_tests(self):
		print('Publishing to PyPi ...')
		os.system("python setup.py bdist_wheel")
		os.system("twine upload dist/hostinfo-{}*.whl".format(VERSION))


setup(
	name="hostinfo",
	version=VERSION,
	author="Kevin Walchko",
	keywords=['system info'],
	author_email="kevin.walchko@outlook.com",
	description="A simple python http server to display basic system information.",
	license="MIT",
	package_data={
		'hostinfo': ['assets/*'],
	},
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 2 :: Only',
		'Operating System :: Unix',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Utilities',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: System :: Shells',
		'Environment :: Console'
	],
	install_requires=['psutil', 'py-cpuinfo', 'simplehtml', 'simplejson', 'qrcode', 'pillow'],
	url="https://github.com/walchko/hostinfo",
	long_description=open('README.rst').read(),
	cmdclass={
		'publish': PublishCommand
	},
	packages=["hostinfo"],
	scripts=[
		'hostinfo/infoserver.py'
	]
)
