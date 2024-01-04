import os
import sys
import struct
from setuptools import setup, find_packages
from distutils.core import Extension
import tarfile
import zipfile
import shutil
import glob
import platform

if sys.version_info >= (3, ):
    from urllib import request
    from io import BytesIO
else:
    import urllib2 as request
    from cStringIO import StringIO as BytesIO

from distutils.sysconfig import get_python_lib
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install

# Writing the Setup Script
# https://docs.python.org/3.4/distutils/setupscript.html#distutils-installing-scripts


print(">>>>>>>> peregrine")


PACKAGE   = 'IfxPy'
VERSION   = '3.0.5'
VERSION2X = '2.7.1'
LICENSE   = 'Apache License 2.0'
IfxPyLongDescription='Informix native Python driver is a high performing data access interface suitable for highly scalable enterprise and IoT solutions to works with Informix database.'

# Python 3.4 and up and not commit to Python 4 support yet
PYTHON_REQ = '~=3.4'

PYTHON_REQ_2X = '>=2.7, <3'


# Specifying the files to distribute
# https://docs.python.org/3.4/distutils/sourcedist.html#manifest
# IfxPy_modules = ['config', 'IfxPyDbi', 'testfunctions', 'tests']
IfxPy_modules = ['IfxPyDbi']


#package_data = { 'IfxPyPkg': [ 'data/IfxPyPackageData1.txt', 'data/IfxPyPackageData2.txt']}
# package_data = { 'IfxPyPkgData': [ 'data/*.txt'] }

# Installing Additional Files
# https://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
# data_files = [ ('IfxPySample', ['./README.rst']),
#                ('IfxPySample', ['../Examples/Sample1.py']),
#                ('IfxPySample', ['../Examples/DbAPI_Sample1.py']),
#                ('IfxPySample', ['../Examples/DbAPI_Sample_executemany.py']),
#                ('IfxPySample', ['../Examples/DbAPI_Sample_Params.py']),
#                ('IfxPySample', ['./LICENSE.txt']) ]

machine_bits =  8 * struct.calcsize("P")
is64Bit = False
prefix = ''

if machine_bits == 64:
    is64Bit = True
    sys.stdout.write("Detected 64-bit Python\n")
else:
    sys.stdout.write("Detected 32-bit Python\n")
	
if('win32' in sys.platform):
	os_ = 'win'
	cliFileName = 'OneDB-Win64-ODBC-Driver.zip'
	prefix = 'build/lib.win-amd64-' + str(sys.version_info[0])+"."+str(sys.version_info[1]) + '/'
elif ('linux' in sys.platform):
	os_ = 'linux'
	cliFileName = 'OneDB-Linux64-ODBC-Driver.tar'
	prefix = 'build/lib.linux-'+ platform.processor() + '-' + str(sys.version_info[0])+"."+str(sys.version_info[1]) + '/'
else:
	cliFileName = 'Unknown'

informixdir = os.getenv('INFORMIXDIR', '')
csdk_home = os.getenv('CSDK_HOME', '')

# Only 64-bit Automated ODBC install is supported, prior installation of CSDK continues to be required for 32-bit 
if is64Bit == True and not informixdir and not csdk_home:
	tmp_path = os.getcwd()
	pip_odbc_path = os.path.join(tmp_path, 'onedb-odbc-driver')
	cpath=''
	cpath1=''

	if not os.path.isdir(pip_odbc_path):
		#url = 'http://127.0.0.1:8000/' + cliFileName
		url = 'https://hcl-onedb.github.io/odbc/' + cliFileName
		sys.stdout.write("Downloading : %s\n" % (url))
		sys.stdout.flush();

		pip_odbc_path = os.path.join(tmp_path, prefix + 'onedb-odbc-driver')
		cpath1 = os.getcwd()
		src = os.path.join(cpath1, prefix + 'onedb-odbc-driver')
		
		file_stream = BytesIO(request.urlopen(url).read())
		if (os_ == 'win'):
			sys.stdout.write("Extracting Windows ODBC files : %s\n" % (url))
			cliDriver_zip = zipfile.ZipFile(file_stream)
			cliDriver_zip.extractall(prefix)
		else:
			sys.stdout.write("Extracting Linux ODBC files : %s\n" % (url))
			cliDriver_tar = tarfile.open(fileobj=file_stream)
			cliDriver_tar.extractall(prefix)
	else:
		cpath = os.getcwd()
		pip_odbc_path = os.path.join(cpath, prefix + 'onedb-odbc-driver')
		if not os.path.isdir(pip_odbc_path):
			#url = 'http://127.0.0.1:8000/' + cliFileName
			url = 'https://hcl-onedb.github.io/odbc/' + cliFileName
			sys.stdout.write("Downloading : %s\n" % (url))
			sys.stdout.flush();

			file_stream = BytesIO(request.urlopen(url).read())
			if (os_ == 'win'):
				sys.stdout.write("Extracting Windows ODBC files : %s\n" % (url))
				cliDriver_zip = zipfile.ZipFile(file_stream)
				cliDriver_zip.extractall(prefix)
				#cliDriver_zip.extractall()
			else:
				sys.stdout.write("Extracting Linux ODBC files : %s\n" % (url))
				cliDriver_tar = tarfile.open(fileobj=file_stream)
				cliDriver_tar.extractall(prefix)
				#cliDriver_tar.extractall()
	
if not informixdir:
	cpath = os.getcwd()
	pip_odbc_path = os.path.join(cpath, prefix + 'onedb-odbc-driver')
	if not os.path.isdir(pip_odbc_path):
		raise ValueError("INFORMIXDIR environment variable must be set!)")
	else:
		informixdir = pip_odbc_path
		
if not csdk_home:
	cpath = os.getcwd()
	pip_odbc_path = os.path.join(cpath, prefix + 'onedb-odbc-driver')
	if not os.path.isdir(pip_odbc_path):
		raise ValueError("CSDK_HOME environment variable must be set!)")
	else:
		csdk_home = pip_odbc_path
		
py_home = os.getenv('MY_PY_DIR', '')
if not py_home:
	cpath = os.getcwd()
	if not os.path.isdir(cpath):
		raise ValueError("MY_PY_DIR environment variable must be set!)")
	else:
		py_home = cpath
		
# Detect CSDK version
# Smart triggers are available from CSDK 4.50/1.0.0.0
vers_csdk_file = os.path.join(informixdir, 'etc', '.lvers_csdk')
csdk_version = None
if os.path.exists(vers_csdk_file):
    with open(vers_csdk_file, 'r') as file:
        csdk_version = file.read().strip().split('.')
else:
    sys.stdout.write("Warning: Could not detect CDSK version.\n")

definitions = []
#OneDB CSDK/ODBC supports Smart Trigger from version 1.0.0.0 onward.
if csdk_version and ( (int(csdk_version[0]) >= 4 and int(csdk_version[1]) >= 50) or (int(csdk_version[0]) == 1 and int(csdk_version[1]) >= 0) ):
    definitions = [('HAVE_SMARTTRIGGER', None)]
    sys.stdout.write("Smart Triggers are enabled.\n")
else:
    sys.stdout.write("Smart Triggers are not available.\n")

if('win32' in sys.platform):
    IfxPyNative_ext_modules = Extension('IfxPy',
        include_dirs = [py_home + '\\include', csdk_home + '\\incl\\cli'],
        libraries = ['iclit09b'],
        define_macros=definitions,
        library_dirs = [ py_home + '\libs', csdk_home + '\lib'],
        sources = ['ifxpyc.c'])
else:
    IfxPyNative_ext_modules = Extension('IfxPy',
        include_dirs = [ py_home,  py_home + '/Include', csdk_home +'/incl/cli'],
        libraries = ['ifdmr', 'thcli'],
        define_macros=definitions,
        library_dirs = [ csdk_home + '/lib/cli', py_home + '/Lib'],
        sources = ['ifxpyc.c'])


# Supporting both Python 2 and Python 3 with Setuptools
# http://setuptools.readthedocs.io/en/latest/python3.html
extra = {}
if sys.version_info < (3, ):
    VERSION    = VERSION2X
    PYTHON_REQ = PYTHON_REQ_2X

setup (name    = PACKAGE,
       version = VERSION,
       license = LICENSE,
       description      = 'Informix native Python driver',
       long_description = IfxPyLongDescription,

       # The project's main homepage.
       #url='https://openinformix.github.io/IfxPy/',
       project_urls={
           'Documentation': 'https://github.com/OpenInformix/IfxPy/wiki',
           'Funding': 'https://openinformix.github.io/IfxPy/',
           'Say Thanks!': 'https://openinformix.github.io/IfxPy/',
           'Source': 'https://github.com/OpenInformix/IfxPy',
           'Tracker': 'https://openinformix.github.io/IfxPy/',
       },
       python_requires = PYTHON_REQ,

       author           = 'Informix Application Development Team',
       #author_email='xyz@hcl.com',

       # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
       classifiers=[
           # How mature is this project? Common values are
           #   3 - Alpha
           #   4 - Beta
           #   5 - Production/Stable
           'Development Status :: 5 - Production/Stable',

           # Indicate who your project is intended for
           'Intended Audience :: Developers',
           'Topic :: Software Development',

           # Pick your license as you wish (should match "license" above)
           'License :: OSI Approved :: Apache Software License',

           # Specify the Python versions you support here. In particular, ensure
           # that you indicate whether you support Python 2, Python 3 or both.
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3.4',
           'Programming Language :: Python :: 3.5',
           'Programming Language :: Python :: 3.6',
           'Programming Language :: Python :: 3.7',
           'Operating System :: Microsoft :: Windows',
           'Operating System :: POSIX',
           'Programming Language :: Python :: Implementation :: CPython',
       ],
       long_description_content_type='text/markdown',

       # What does your project relate to?
       keywords='Informix Python Enterprise TimeSeries IoT',

       ext_modules = [IfxPyNative_ext_modules],
       py_modules   = IfxPy_modules,
    #    package_data = package_data,
    #    data_files   = data_files,
    #    include_package_data = True,
       **extra
      ) 

