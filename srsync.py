#!/usr/bin/env python
# import the os module
import os
import json
import subprocess
import shutil
#	This script will sync a directory with your SR's.
#		Open SR's will have a directory created and closed SR's
#		will have their directories moved to a "Closed" 
#		Directory.
#
# ************************************************************************
# Ask for the username of the Service Request Owner to sync:
#
# And ask for the path to their gwsupport folder.
# ************************************************************************
 
#user = raw_input("Username: ")

# if (input("Is the script in your gwsupport directory? (y/n)") == 'y'):
# 	path = os.getcwd()
# else:
# 	path = input("Please enter the full path to your gwsupport directory: ")

#print 'Your name is ' + user
# print(path)
#
#	1. First, check if the open and closed dir's exists, if they don't: 
# 				create the "open" directory
#				create the "closed" directory
#
os.path.exists("open") or os.mkdir("open")
os.path.exists("closed") or os.mkdir("closed")
#			
#
#		
#		
#	a line to put the SR info into a variable
result = os.popen("curl http://proetus.provo.novell.com/qmon/brief-tse-json.asp?tse=cthomas").read()
# *** Parse the string into a json object for reading
json_srs = json.loads(result)

openSrs = {}
for i in range(len(json_srs)):
	openSrs[i] = json_srs[i]['SR']
#			
#		 
#	Create a list of directories excluding closed and open
# by assigning to the slice list[:] you can mutate the existing list to contain only the items you want
allFolders = os.listdir(os.getcwd())
allFolders[:] = [x for x in allFolders if not os.path.isfile(x) and not x == 'open' and not x == 'closed']

# compare all folders against openSrs, when they match, send to open, else, send them to closed


for x in allFolders:
	for i in openSrs:
		if x == openSrs[i]:
			try:
				print("Moving: " + x + " to open")
				shutil.move(x, "open/")
				break
			except Exception:
				print(x + " something went wrong, duplicate directory name probably, here's there error: ")
				print(Exception)
		else:
			if i == len(openSrs) - 1:
				try:
					print("Moving: " + x + " to closed")
					shutil.move(x, "closed/")
				except Exception:
					print(x + " something went wrong, duplicate directory name probably, here's there error: ")
					print(Exception)



# this line moves everything other than closed, open, and srsync into open... might not use it.
#subprocess.check_call(["bash", "-O", "extglob", "-c", "mv !(closed|open|srsync.py) open"])


# *****************************************************************************************************
#  clear up the allFolders variable as it doesn't serve any purpose anymore
del allFolders
#			
#				
#			os.chdir()  #move focus to a different dir
# *********************************************************************************************************
#  At this point we've sorted existing directories to closed, and open. Now create new dirs in open
#  when an open sr doesn't already have a directory there.

os.chdir(os.getcwd() + "/open")

#
# create a new list of folders in current directory
openFolders = os.listdir(os.getcwd())


# for loop to verify the openSr has a directory for it, if it doesn't create one.
	for i in openSrs:
		if not os.path.isdir(os.getcwd() + "/" + openSrs[i]):
			print(openSrs[i] + " doesn't exist, let's make it")
			os.mkdir(openSrs[i])


# 	You can use list comprehension to create a new list containing only the elements you DON'T want to remove
# somelist = [x for x in somelist if not determine(x)]

# or by assigning to the slice list[:] you can mutate the existing list to contain only the items you want



#
#	4. step through all of the openFolders and move folders that 
# 		aren't in the opensrs list anymore to closed.
#	
def moveToClosed(openList, currentList):
	try:
		move = False
		for i in currentList:
			for x in openList:
				if i == x:
					break
				elif x == len(openList) - 1:
					print("Moving: " + i + " to closed")
					shutil.move(i, "closed/")
		
		
	except Exception:
		print(Exception)
# 		
#		
#		recursively remove empty directories with 'os.rmdirs()'
#			os.removedirs('dir_a/dir_b/dir_c')
#		
#
#
#		
