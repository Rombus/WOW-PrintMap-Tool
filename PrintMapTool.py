# PrintMap JSON Tool
# Creates a GeoJSON file with a given Lat, Long and Map Details
# Map Number = RRCC (RowRowColumnColumn)
# good montgomery base point? 32.348738, -86.361760 print 4435

import LatLongMath
import FileData
import geojson
# User Input requests to setup map numbering scheme

directory = input("What print directory do you want to create a PrintMap for?")
knownMap = input("What map location is the base Lat Long: ")
knownLat = float(input("What is the Latitude for the known upper left corner of print {} :".format(knownMap)))
knownLong = float(input("What is the Longitude for the known upper left corner of print {} :".format(knownMap)))
width = int(input("How wide (in feet) is each print: "))
length = int(input("How long (in feet) is each print: "))
knownRow = int(knownMap[0:2])
knownCol = int(knownMap[2:4])

FD = FileData.FileData(directory)

colFtToZero = int(FD.colStepsToZero(knownCol)) * width
rowFtToZero = int(FD.rowStepsToZero(knownRow)) * length

originArray = LatLongMath.FindOrigin([knownLong, knownLat], rowFtToZero, colFtToZero)


# Create a list of what each X and Y Value label could be
rowValues = list(range(FD.minRow(), FD.maxRow()+FD.rowStep, FD.rowStep))
colValues = list(range(FD.minCol(), FD.maxCol()+FD.colStep, FD.colStep))
rowValues.reverse()

mapGrid = LatLongMath.generateGridMatrix(originArray, len(rowValues), len(colValues), length, width)

# Build a dictionary of Row/Columns with the appropriate coordinates
mapDictionary = {}

for R in range(len(rowValues)):
    for C in range(len(colValues)):
        # Need to follow the right hand rule UR, UL, LL, LR, UR
        thisBox = [[mapGrid[R][C+1],
                    mapGrid[R][C],
                    mapGrid[R + 1][C],
                    mapGrid[R + 1][C + 1],
                    mapGrid[R][C + 1]]]
        mapDictionary[repr(rowValues[R])+repr(colValues[C])] = thisBox

print(len(mapDictionary))
sorted(mapDictionary.keys())
geoJsonFeatures = []

for k, v in mapDictionary.items():
    if str(k + ".dwg") in FD.printList:
        thisPolygon = geojson.Polygon(v)
        thisFeature = geojson.Feature(geometry=thisPolygon, id=k, properties={"id": k, "link": str(directory + "\\" + k + ".dwg")})
        geoJsonFeatures.append(thisFeature)


geoJsonComplete = geojson.FeatureCollection(geoJsonFeatures)

validation = geojson.is_valid(geoJsonComplete)

print(validation['valid'])
print(validation['message'])

print("Writing File")
f = open("GeoJsonOutput", "w")
geojson.dump(geoJsonComplete, f)
f.close()
