# This is going to be the setup script for the srsync script
# 
# 	1. Prompt user for their username
#		Prompt for full path to directory to be synced.
#   2. Create config file with full path to user's home folder
#		grab a list of folders in /files/ and check for
#       a folder that matches username. Use that if it exists
#		and if not, ask for a path to sync sr folders
#
#	3. Run srsync.py
#	4. setup check.py to run every few seconds
#			and for it to check the correct list of
#			open SRs in the correct path.
# 		Create a cron.d entry in /etc/cron.d to run the check
#			script at a random time for the user and path in
#			their config file.
#
# ***********************************************************
# setup.py 
# ***********************************************************
#  import statements
import ConfigParser
import srsync
import subprocess
import readline

def completer(text, state):
    options = [i for i in commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

#
# 1. Get input from user
#
user = str(raw_input('Username: '))
pathinput = str(raw_input('Enter full path to your Service Request directory: '))

# 2. Set up the Config file with the username and path
config = ConfigParser.ConfigParser()
config.add_section('main')
config.set('main', 'username', user)
config.set('main', 'path', pathinput) 
				  
with open('config.ini', 'w') as configfile:
	config.write(configfile)


# Getting info from the config file:
# 
# import configparser
# config = configparser.ConfigParser()
# config.read('config.ini')
# username = config['main']['username']
# path = config['main']['path']

# 3. call main from srsync
srsync.main()

# 4. set up job to run srsync.py
# doesn't have to be every minute, but do it during the hours of the workday
# * * * * * root pathinput + /safe/srsync.py >/dev/null 2>&1
file = open(crontab, 'a')
file.write('* * * * * root {pathinput} /safe/srsync.py >/dev/null 2>&1')
file.close()

