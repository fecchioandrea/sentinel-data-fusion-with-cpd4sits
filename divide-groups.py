"""
	execute.py
	Author: Andrea Fecchio, 2021
"""

import os
import random
import shutil

set30 = [ ]
set70 = [ ]

path = "C:/Users/fecch/Desktop/UNIPV/Magistrale/Laurea/Tesi/cpd4sits/polygons-v5"
polygons = os.listdir(path + "/pol30")

def mkdir():
	os.mkdir(path + "/test70/")
	os.mkdir(path + "/test30/")

#
# Random choice of polygons
#

def randchoice():
	global set30
	global set70
	set30 = random.sample(polygons, 30)
	for elem in polygons:
		if elem not in set30:
			set70.append(elem)

#
# Assignment of train and test sets
#

def assign():
	for polygon in set30:
		os.mkdir(path + "/test30/" + polygon)
		files = os.listdir(path + "/pol30/" + polygon)
		for file in files:
			os.rename("./pol30/" + polygon + "/" + file, "./test30/" + polygon + "/" + file)
	for polygon in set70:
		os.mkdir(path + "/test70/" + polygon)
		files = os.listdir(path + "/pol30/" + polygon)
		for file in files:
			os.rename("./pol30/" + polygon + "/" + file, "./test70/" + polygon + "/" + file)


# ----------------------------------------------------------------------

def main():
	mkdir()
	randchoice()
	assign()
	print("Completed.")


# Driver Function
if __name__ == '__main__':
    main()

