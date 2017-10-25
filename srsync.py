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
#		Shane suggests using the request library so that I can pull the json info from 
# 		the url without using the os library, apparently it can be really slick.
#		also, I'd have to put the request library somewhere for the script to access it.
#		  
#		First, check if the open and closed dir's exists, if they don't: 
# 				create the "open" directory
#				create the "closed" directory
#
def maybeCreateFolder(string):
	os.path.exists(string) or os.mkdir(string)
#			
#
#		
#	
def getNameOfDir():
	# this splits the full path by /, and then returns the last item.
	#return the string "name of the dir" or "username of engineer"
	return os.getcwd().split('/')[-1]

def getSrList(user):
	#	a line to put the SR info into a variable
	result = os.popen("curl http://proetus.provo.novell.com/qmon/brief-tse-json.asp?tse=%s" % user).read()
	# *** Parse the string into a json object for reading
	json_srs = json.loads(result)

	openSrs = {}
	for i in range(len(json_srs)):
		openSrs[i] = json_srs[i]['SR']
	return openSrs
#			
#		 
#	Create a list of directories excluding closed and open
# by assigning to the slice list[:] you can mutate the existing list to contain only the items you want
def getFolderList():
	allFolders = os.listdir(os.getcwd())
	allFolders[:] = [x for x in allFolders if os.path.isdir(x) and not x == 'open' and not x == 'closed']
	return allFolders

# compare all folders against openSrs, when they match, send to open, else, send them to closed

def organizeFolders(folders, srs):
	for x in folders:
		for i in srs:
			if x == srs[i]:
				try:
					print("Moving: " + x + " to open")
					shutil.move(x, "open/")
					break
				except Exception:
					print(x + " something went wrong, duplicate directory name probably, here's there error: ")
					print(Exception)
			else:
				if i == len(srs) - 1:
					try:
						print("Moving: " + x + " to closed")
						shutil.move(x, "closed/")
					except Exception:
						print(x + " something went wrong, duplicate directory name probably, here's there error: ")
						print(Exception)



# for loop to verify the openSr has a directory for it, if it doesn't create one.
def createOpenDir(openList):
	for i in openList:
		if not os.path.isdir(os.getcwd() + "/" + openList[i]):
			print(openList[i] + " doesn't exist, let's make it")
			os.mkdir(openList[i])

#	4. step through all of the openFolders and move folders that 
# 		aren't in the opensrs list anymore to closed.
#	
def moveToClosed(openList, currentList):
	try:
		for i in currentList:
			for x in openList:
				if i == openList[x]:
					break
				elif x == len(openList) - 1:
					print("Moving: " + i + " to closed")
					shutil.move(i, "../closed/")
		
		
	except Exception:
		print("moveToClosed: ", Exception)


# ****************************************************************
# Main:
#
# This will control the sequence of events.
#
# ****************************************************************
def main():
	""" Main controller """

	# open and closed folders?
	maybeCreateFolder('open')
	maybeCreateFolder('closed')

	# get username or name of current directory, get list of SR's, get list of 
	# folders in current directory, and sort them to open or closed
	username = getNameOfDir()
	organizeFolders(getFolderList(), getSrList(username)) 

	# change to the open directory
	os.chdir(os.getcwd() + "/open")

	# create dirs for each open SR if it's not already there.
	createOpenDir(getSrList(username))

	# create a new list of folders in current directory (which is 'open' right now)
	openFolders = os.listdir(os.getcwd())

	# make sure to move closed SR folders out of open
	moveToClosed(getSrList(username), openFolders)


if __name__ == "__main__":
	main()