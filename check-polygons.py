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

array = [ ["10","1","VV_66-VH-NDVI"], ["10","1","VV_66-NDVI"], ["7","31","VV_66-NDVI"], ["10","1","VV_66-VH_66-NDVI"], ["7","91","VV_66-NDVI-SBI"], ["7","31","NDVI"], ["7","31","VV_66-NDBI-SBI"], ["7","61","VV_66-NDVI"], ["7","31","VV-NDVI"], ["10","31","VV_66-VH-NDVI-NDBI"], ["7","61","VV_66-NDVI-NDBI"], ["10","1","VV_66-NDBI-SBI"], ["10","31","VV_66-NDVI-NDBI"], ["7","31","NDBI-SBI"], ["7","61","VV_66-NDVI-SBI"], ["7","91","VV_66-VH_66-NDVI-SBI"], ["10","1","VV_66-VH_66-NDBI-SBI"], ["10","31","NDVI-NDBI"], ["10","31","VV_66-VH_66-NDVI-NDBI"], ["10","1","VH-NDBI-SBI"], ["10","1","VV-VH-NDBI-SBI"], ["10","31","VV-NDVI-NDBI"], ["10","31","VH-NDVI-NDBI"], ["7","91","VV_66-VH-NDVI-SBI"], ["3","91","VV_66-VH-SBI"], ["3","91","VV_66-VH_66-SBI"], ["5","61","VV_66-VH_66-SBI"], ["5","91","VV_66-VH_66-SBI"], ["5","91","VV_66-NDBI-SBI"], ["7","1","VV_66-NDBI"], ["7","61","VV_66-NDVI-NDBI-SBI"], ["7","91","VV_66-VH_66-NDVI"], ["10","1","VH_66-NDVI"], ["10","31","VV_66-VH_66-NDVI"], ["10","31","VV_66-VH_66-NDVI-SBI"], ["10","91","VV_66-NDVI-NDBI-SBI"], ["5","91","VV-NDVI-NDBI-SBI"], ["7","31","VH-NDVI"], ["10","1","VV-NDVI"], ["10","1","VV-VH-NDVI"], ["10","31","VV-VH-NDVI-NDBI"], ["10","1","VH-VV_66-NDBI-SBI"] ]

# ---------------------------------------------------------------------------

path = "C:/Users/fecch/Desktop/UNIPV/Magistrale/Laurea/Tesi/cpd4sits/polygons-v5"

polygons = os.listdir(path + "/test30") + os.listdir(path + "/test70")

#
# Computing statistics
#

def statistics(polygons,array):
	reality = False
	changes = False
	tp = [0] * len(polygons)
	fp = [0] * len(polygons)
	tn = [0] * len(polygons)
	fn = [0] * len(polygons)
	data = { "TP":[], "FP":[], "FN":[], "TN":[] }
	index = []
	combs = len(array)
	for polygon in polygons:
		if polygon.startswith("mod"):
			reality = True
		elif polygon.startswith("unmod"):
			reality = False
		ind = polygons.index(polygon)
		for i in range(combs):
			penalty = array[i][0]
			window = array[i][1]
			feature = array[i][2]
			id = "c30-g150-p" + penalty + "-w" + window + "-" + feature + ".csv"
			filepath = "./results/" + polygon + "/" + polygon + "_dates-" + id
			filedim = os.path.getsize(filepath)
			if filedim == 12:
				changes = False
			elif filedim > 12:
				changes = True
			if reality and changes:
				tp[ind] +=1
			elif reality and not changes:
				fn[ind] +=1
			elif not reality and changes:
				fp[ind] +=1
			else:
				tn[ind] +=1
			
		index.append(polygon)
		data["TP"].append(tp[ind])
		data["FP"].append(fp[ind])
		data["FN"].append(fn[ind])
		data["TN"].append(tn[ind])
	df = pd.DataFrame(data, index = index)
	df.to_csv('pol-res-complete.csv')


# ----------------------------------------------------------------------

def main():
	statistics(polygons,array)


# Driver Function
if __name__ == '__main__':
    main()

