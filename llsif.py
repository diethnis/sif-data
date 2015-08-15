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
	output = 'JSONDATA from '.format(url)
	return output

def getUnitData(unitno):
	print('call to getJSONData')
	return getJSONData('asdf')

currtime = getTime()

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
	args.host = input('FTP server (default \'{}\'): '.format(host_default))
	if not args.host:
		logger.debug('Default server used: {}'.format(host_default))
		args.host = host_default
while not args.username:
	args.username = input('FTP server username: ')
while not args.password:
	args.password = getpass.getpass('FTP server password: ')
logger.debug('Got credentials. HOST: {} USERNAME: {} PASSWORD: {}'.format(args.host, args.username, '*' * len(args.password)))

print('Testing user input.')
try:
	unitno = 0+int(input('Enter a unit number to look up: '))
except:
	print('Invalid input; default number used: 136')
	unitno = 136


print('Testing API call and GET request for unit {}.'.format(unitno))
url = 'http://schoolido.lu/api/cards/{}/'.format(unitno)
rawpagedata = requests.get(url)
encoding = rawpagedata.headers['content-type']
if 'utf' in encoding.lower() and '8' in encoding:
	pagedata = rawpagedata.content.decode('UTF-8')
else:
	pagedata = rawpagedata.content.decode('Windows-1257')
input('Testing JSON parsing.')
jsondata = json.loads(pagedata)
print(json.dumps(jsondata['idol'], sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False))
input('\n\n')
yamldata = yaml.safe_dump(jsondata, allow_unicode=True)
print(yamldata)

print('.temp_llsif_{}'.format(currtime))

#with pysftp.Connection(host=args.host, username=args.username, password=args.password) as sftp:
#	print(sftp.listdir())
#	print(sftp.pwd)
#	sftp.close()
#	# docs:  http://pysftp.readthedocs.org/en/release_0.2.8/

# git commit -m 'Edit summary or comment'
# git push origin master
# stackoverflow.com/questions/7225900/
# github.com/robbyrussell/oy-my-zsh