#!/bin/bash
# convert.sh
# Ver. 1.0, Reldate 2021-08-27
# (C) Andrea Fecchio, 2021

# This application let us automate a series of command line operations, in order to extract the SHP files from the polygons, which were exported as KMZ files from Google Earth Pro.

# Structure:
#		.
#		|______ /polygons/
#		|	|______ *.kmz
#		|	|
#		|	|______ /shp/
#		|		|______ *.zip
#		|
#		|______ convert.sh

# Input (in ./polygons/):		70* mod_0xx_aaa.kmz
#					70* unmod_1xx_a.kmz
	
# Output (in ./polygons/shp/):		70* mod_0xx_aaa.zip
#					70* unmod_1xx_a.zip

# Working:
#	sudo apt-get install gdal-bin
#	cd ./Scrivania/luoghi/
#	chmod +x convert.sh
#	./convert.sh

cd ./polygons/

for i in *.kmz; do

	filename="${i%.*}"

	cp "${filename}.kmz" "${filename}.zip"
	unzip "${filename}.zip"
	mv doc.kml "shp/${filename}.kml"
	ogr2ogr -f 'ESRI Shapefile' "shp/${filename}.shp" "shp/${filename}.kml"
	zip "shp/${filename}.zip" "shp/${filename}.shp" "shp/${filename}.shx" "shp/${filename}.dbf" "shp/${filename}.prj"
	
	rm "./${filename}.zip" "shp/${filename}.kml" "shp/${filename}.shp" "shp/${filename}.shx" "shp/${filename}.dbf" "shp/${filename}.prj"
	echo "Done with $filename";
done

