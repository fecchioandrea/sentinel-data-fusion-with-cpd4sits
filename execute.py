"""
	execute.py
	Author: Andrea Fecchio, 2021
"""

from itertools import combinations as comb
import os
import pandas as pd

#
# Indices combination preparation
#

penalty_array = ["3","5","7","10"]
window_array = ["1","31","61","91"]

possible_features_array = ["VV_66", "VH_66", "NDVI", "NDBI", "SBI"]		# first launch
# possible_features_array = ["VV", "VH", "NDVI", "NDBI", "SBI"]			# second launch

features_array = []

def prepare_features_array():
	array = []
	features = []
	for i in range(1, len(possible_features_array)+1):
		els = [list(x) for x in comb(possible_features_array, i)]
		array.extend(els)
	
	ind = ""
	for i in range(len(array)):
		ind = ""
		num = len(array[i])
		for j in range(num):
			ind += array[i][j]
			ind += "-"
		features.append(ind[:-1])
	
	return features


# ---------------------------------------------------------------------------

path = "C:/Users/fecch/Desktop/UNIPV/Magistrale/Laurea/Tesi/cpd4sits/polygons-v5"

polygons = os.listdir("./test30/")

def mkdir():
	for polygon in polygons:
		os.mkdir("./results/" + polygon)


#
# Launch cpd4sits for each polygon
#

def cpd4sits(polygon,penalty,window,feature):
	os.system("docker run --rm -v " + path + "/test30:/usr/src/app/data cpd4sits -s 2017-01-01 -e 2020-12-31 -g 150 -p " + penalty + " -w " + window + " data/" + polygon + " " + feature)
	os.rename("./test30/" + polygon + "/" + polygon + "_dates.csv", "./results/" + polygon + "/" + polygon + "_dates-c30-g150-p" + penalty + "-w" + window + "-" + feature + ".csv")
	os.rename("./test30/" + polygon + "/" + polygon + "_features.csv", "./results/" + polygon + "/" + polygon + "_features-c30-g150-p" + penalty + "-w" + window + "-" + feature + ".csv")


def cpd4sits_cycle(polygons):
	for penalty in penalty_array:
		for window in window_array:
			print("\nStarting cpd4sits with penalty " + penalty + " and window " + window + "...")
			for feature in features_array:
				print("Starting with features " + feature + "...")
				for polygon in polygons:
					cpd4sits(polygon,penalty,window,feature)
	print("\n\nAll polygons elaborated.\n\n")


#
# Computing statistics
#

reality = False
changes = False
tp = 0
fp = 0
tn = 0
fn = 0
tpr = 0.0
fpr = 0.0

data = { "TP":[], "FP":[], "FN":[], "TN":[], "TPR":[], "FPR":[], "F1-score":[] }
index = []

def statistics():
	for penalty in penalty_array:
		for window in window_array:
			for feature in features_array:
				tp = 0
				fp = 0
				tn = 0
				fn = 0
				id = "dates-c30-g150-p" + penalty + "-w" + window + "-" + feature + ".csv"
				for polygon in polygons:
					if polygon.startswith("mod"):
						reality = True
					elif polygon.startswith("unmod"):
						reality = False
					filepath = "./results/" + polygon + "/" + polygon + "_" + id
					filedim = os.path.getsize(filepath)
					if filedim == 12:
						changes = False
					elif filedim > 12:
						changes = True
					if reality and changes:
						tp+=1
					elif reality and not changes:
						fn+=1
					elif not reality and changes:
						fp+=1
					else:
						tn+=1
			
				index.append(id[:-4])
				data["TP"].append(tp)
				data["FP"].append(fp)
				data["FN"].append(fn)
				data["TN"].append(tn)
				tpr = tp/(tp+fn)
				data["TPR"].append(tpr)
				fpr = fp/(fp+tn)
				data["FPR"].append(fpr)
				f1 = tp/(tp + (fp+fn)/2)
				data["F1-score"].append(f1)

	return pd.DataFrame(data, index = index)


# ----------------------------------------------------------------------

def main():
	global features_array
	features_array = prepare_features_array()
	# print(features_array)
	# print(str(len(features_array)) + " features disponibili.")
	
	# mkdir()
	
	# cpd4sits_cycle(polygons)
	
	df = statistics()
	print(df)
	df.to_csv('results.csv', float_format='%.2f')


# Driver Function
if __name__ == '__main__':
    main()

