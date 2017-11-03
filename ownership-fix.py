# owndership-fix.py
import os

# This script will fix the ownership of folders created by older
# versions of the SRSync script that created folders and didn't change
# the user:group from root:root to gwsupport:users. 
# 
# it'll loop through the current folders and if their ownership isn't
# correct then it'll change it.
#
# Just put this script in the open directory and it'll fix them
# 
#
# getFolderList()
# 	returns a list of all the folders in the current dir (open)
#
def getFolderList():
	allFolders = os.listdir(os.getcwd())
	allFolders[:] = [x for x in allFolders if os.path.isdir(x)]
	return allFolders
#
# changeOwnership(list_of_folders)
# 	receives a list of folders you want it to check and fix
def changeOwnership(folderList):
	for i in folderList:
		if ((os.stat(i).st_uid != 1002) or (os.stat(i).st_gid != 100)):
			os.chown(i, 1002, 100)
			print("change")

#
# *******************************************************
#
# Main
#
# *******************************************************
#
def main():
	currentFolders = getFolderList()
	print(currentFolders)
	changeOwnership(currentFolders)

if __name__ == "__main__":
	main()