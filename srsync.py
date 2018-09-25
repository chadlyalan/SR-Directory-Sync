#!/usr/bin/env python
# import the os module
import os
import json
import subprocess
import shutil
import ConfigParser

#	This script will sync a directory with your SR's.
#		Open SR's will have a directory created and closed SR's
#		will have their directories moved to a "Closed" 
#		Directory. 
#
#*********************************************************************
# VERSION 1.03
#*********************************************************************
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
	os.chown(string, 1002, 65534)

#			
#
#	
def getNameOfDir():
	# this splits the full path by /, and then returns the last item.
	#return the string "name of the dir" or "username of engineer"
	return os.getcwd().split('/')[-1]


def getSRInfo(user):
	#	a line to put the SR info into a variable
	result = os.popen("curl -s http://proetus.provo.novell.com/qmon/brief-tse-json.asp?tse=%s" % user).read()
	# *** Parse the string into a json object for reading and return it
	return json.loads(result)

def getSrList(user):
	json = getSRInfo(user)

	openSrs = {}
	for i in range(len(json)):
		openSrs[i] = json[i]['SR']
	return openSrs

#
# this is going to get a brief description of an SR
#
def getBriefDesc(user):
	json = getSRInfo(user)

	briefDesc = {}
	for i in range(len(json)):
		briefDesc[i] = json[i]['BRIEF']
	return briefDesc



#			
#		 
#	Create a list of directories excluding closed and open
# by assigning to the slice list[:] you can mutate the existing list to contain only the items you want
def getFolderList(path):
	allFolders = os.listdir(path)
	allFolders[:] = [x for x in allFolders if os.path.isdir(x) and not x == 'open' and not x == 'closed'and not x == 'safe']
	return allFolders

# compare all folders against openSrs, when they match, send to open, else, send them to closed

def organizeFolders(path, folders, srs):
	for x in folders:
		for i in srs:
			if x == srs[i]:
				try:
					print("Moving: " + x + " to open")
					shutil.move(path + x, path + "open/")
					break
				except Exception:
					print(x + " something went wrong, duplicate directory name probably, here's there error: ")
					print(Exception)
			else:
				if i == len(srs) - 1:
					try:
						print("Moving: " + x + " to closed")
						shutil.move(path + x, path + "closed/")
					except Exception:
						print(x + " something went wrong, duplicate directory name probably, here's there error: ")
						print(Exception)



# for loop to verify the openSr has a directory for it, if it doesn't create one.
def createOpenDir(path, openList, briefList):
	for i in openList:
		
		if not os.path.isdir(path + openList[i]):
		# (if a directory named after it's SR number + brief doesn't exist: then create it)
			if not (os.path.isdir(path + openList[i] + ' - ' + briefList[i])):
				print(openList[i] + ' - ' + briefList[i] +" doesn't exist, let's make it")
				os.mkdir(path + openList[i] + ' - ' + briefList[i])
				os.chown(path + openList[i] + ' - ' + briefList[i], 1002, 65534)
				# this should change the ownership to user:gwsupport group:users
				# like the rest of the folders created
		
		# this else represents the use case (if SR folder w/o brief description exists): rename it
		else:
			#if a dir named after this SR does exist already, append brief description of SR:
			os.rename(path + openList[i], path + openList[i] + ' - ' + briefList[i])



#	4. step through all of the openFolders and move folders that 
# 		aren't in the opensrs list anymore to closed.
#	
def moveToClosed(path, openList, currentList, briefList):
	try:
		for i in currentList:
			for x in openList:
				if i == (openList[x] + ' - ' + briefList[x]):
					break
				elif x == len(openList) - 1:
					try:
						os.rmdir(path + i)
						srName = (i, " is empty, deleted!")
						print srName
					except OSError as ex:
						print(i + " is not empty, moving to closed")
						shutil.move(path + i, path + "../closed/")
		
		
	except Exception:
		print("moveToClosed: ", Exception)

#def checkForCharacters(briefList):
	# if we find any of these special characters in the brief description, remove them.
	#
	#


# ****************************************************************
# Main:
#
# This will control the sequence of events.
#
# ****************************************************************
def main():
	""" Main controller """
	# 	Config file variables and username variable
	config = ConfigParser.ConfigParser()
	config.read('config.ini')
	username = config.get('main','username')
	path = config.get('main','path')

	# open and closed folders?
	maybeCreateFolder(path + 'open')
	maybeCreateFolder(path + 'closed')
	maybeCreateFolder(path + 'safe')

	# get list of SR's, get list of 
	# folders in sync directory, and sort them to open or closed
	srList = getSrList(username)
	organizeFolders(path, getFolderList(path), srList) 

	# change to the open directory
	# ^ doesn't really apply anymore
	# instead we'll update the path to include the open dir
	path = path + 'open/'

	brief = getBriefDesc(username)
	# create dirs for each open SR if it's not already there.
	createOpenDir(path, srList, brief)

	# create a new list of folders in the open directory
	openFolders = os.listdir(path)

	# make sure to move closed SR folders out of open
	moveToClosed(path, srList, openFolders, brief)


if __name__ == "__main__":
	main()