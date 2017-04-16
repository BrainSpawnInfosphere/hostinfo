from setuptools import setup
from hostinfo.version import __version__ as VERSION
from build_utils import BuildCommand
from build_utils import PublishCommand
from build_utils import BinaryDistribution


PACKAGE_NAME = 'hostinfo'
BuildCommand.pkg = PACKAGE_NAME
# BuildCommand.py3 = False
PublishCommand.pkg = PACKAGE_NAME
PublishCommand.version = VERSION
README = open('README.rst').read()


setup(
	name=PACKAGE_NAME,
	version=VERSION,
	author="Kevin J. Walchko",
	keywords=['system info'],
	author_email="kevin.walchko@outlook.com",
	description="A simple python http server to display basic system information.",
	license="MIT",
	package_data={
		'hostinfo': ['static', 'templates'],
	},
	include_package_data=True,
	zip_safe=False,
	classifiers=[
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Programming Language :: Python :: 2.7',
		'Programming Language :: Python :: 3.6',
		'Operating System :: Unix',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: POSIX',
		'Topic :: Utilities',
		'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
		'Topic :: System :: Shells',
		'Environment :: Console'
	],
	install_requires=open("requirements.txt").readlines(),
	url="https://github.com/walchko/{}".format(PACKAGE_NAME),
	long_description=README,
	cmdclass={
		'publish': PublishCommand,
		'make': BuildCommand
	},
	packages=[PACKAGE_NAME],
	scripts=[
		'bin/hostinfoserver.py'
	]
)
