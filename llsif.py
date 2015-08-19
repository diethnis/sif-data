import argparse # runtime flags
import pysftp # pip install pysftp
import requests # replace with human_curl?
import json
import yaml # pip install pyyaml, replaces json
import logging # logs for verbosity
import getpass # hidden password input
from time import strftime
# check module versions with pip freeze
# GUI from tkinter or pyqt, or use HTML pages
# implement classes for OOP/ per unit data

def getTime():
	return strftime('%Y%m%d%H%M%S')

def getJSONData(url):
	rawpagedata = requests.get(url)
	encoding = rawpagedata.headers['content-type']
	if 'utf' in encoding.lower() and '8' in encoding:
		pagedata = rawpagedata.content.decode('UTF-8')
	else:
		pagedata = rawpagedata.content.decode('Windows-1257')
	jsondata = json.loads(pagedata)
	return jsondata

def getUnitData(unitno):
	url = 'http://schoolido.lu/api/cards/{}/'.format(unitno)
	return getJSONData(url)

def loadFromFile(sftp):
	if not sftp.exists(datafile) and sftp.isfile(datafile):
		print('Do something')
#	handle multiple accounts/servers?

class Units(object):
	def __init__(self, accountName, server='jp'):
		pass
	def createEmptyServer(self, accountName, server='jp'):
		pass
	def addHand(unitno):
		pass
	def delHand(unitno):
		pass
	def updateHand(uniqueID):
		pass
	def addAlbum(inp):
		# parse unitno and status (idolized, maxlevel, kizuna)
		pass
	def delAlbum(unitno):
		pass

# how even class? lel

# del dict['key'] removes elements
# * prefix splats lists/tuples
# ** prefix splats dictionaries; use with .format by {key}

currtime = getTime()
datafile = 'sifdata.yaml'

parser = argparse.ArgumentParser(description='Check and update LLSIF unit data')
parser.add_argument('-v', '--verbose', action='count', default=0,
					help='Increase output verbosity')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-n', '--noact', action='store_true',
					help='Do nothing. Check data on FTP server')
group.add_argument('-u', '--update', action='store_true',
					help='Upload data to FTP server')
parser.add_argument('host', nargs='?',
					help='The address of the FTP server')
parser.add_argument('username', nargs='?',
					help='The username used for the FTP server')
parser.add_argument('password', nargs='?',
					help='The password used for the FTP server')
args = parser.parse_args()

if args.verbose:
	if args.verbose == 1:
		logging.basicConfig(level=logging.INFO)
	else:
		logging.basicConfig(level=logging.DEBUG)
else:
	logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)

# pass keyword to skip an except in try/except

logger.info('Prompt for FTP server credentials')
host_default = 'homepages.wmich.edu'
if not args.host:
	args.host = input('FTP server: ')
	if not args.host:
		logger.info('Default server used: {}'.format(host_default))
		args.host = host_default
while not args.username:
	args.username = input('FTP server username: ')
while not args.password:
	args.password = getpass.getpass('FTP server password: ')
logger.debug('Got credentials. HOST: {} USERNAME: {} PASSWORD: {}'.format(
		args.host, args.username, '*' * len(args.password)))

credentials = {'host':args.host, 'port':22, 'username':args.username, 'password':args.password}

# create loop for CLI menu navigation

if args.noact:
	logger.info('Check data on FTP server; logging in')
	with pysftp.Connection(**credentials) as sftp:
		tempdata = loadFromFile(sftp)
		if not sftp.exists('sifdata.yaml'): # also .isfile()
			logger.info('sifdata.yaml does not exist on the remote server')
		print(sftp.listdir())
		print(sftp.pwd)

else:
	logger.info('Update data on FTP server; logging in')
	with pysftp.Connection(**credentials) as sftp:
		if not sftp.exists('sifdata.yaml'): # also .isfile()
			logger.info('sifdata.yaml does exist on the remote server')


logger.debug('Testing user input.')
try:
	unitno = 0+int(input('Enter a unit number to look up: '))
except:
	logger.debug('Invalid input; default number used: 136')
	unitno = 136


logger.info('Testing API call and GET request for unit {}.'.format(unitno))
logger.info('Testing JSON parsing.')
print(json.dumps(getUnitData(unitno)['idol'], sort_keys=False, indent=4,
		separators=(',', ': '), ensure_ascii=False))
input('\n\n')
yamldata = yaml.safe_dump(getUnitData(unitno), allow_unicode=True)
print(yamldata)

print('.temp_llsif_{}'.format(currtime))

# see ~/testweb.py for creating temp HTML file

# docs:  http://pysftp.readthedocs.org/en/release_0.2.8/

# stackoverflow.com/questions/7225900/
# rogerdudler.github.io/git-guide/
