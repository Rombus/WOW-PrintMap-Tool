# PrintMap JSON Tool
# Creates a GeoJSON file with a given Lat, Long and Map Details
# Map Number = RRCC (RowRowColumnColumn)
# good montgomery base point? 32.348738, -86.361760 print 4435

import LatLongMath
import geojson
# User Input requests to setup map numbering scheme

startRow = int(input("What is the lowest map row number: "))
endRow = int(input("What is the highest map row number: "))
stepRow = int(input("How many steps between each row: "))
startCol = int(input("What is the lowest map column number: "))
endCol = int(input("What is the highest map column number: "))
stepCol = int(input("how many steps between each column: "))
knownMap = input("What map location is the base Lat Long: ")
knownLat = float(input("What is the Latitude for the known upper left corner of print {} :".format(knownMap)))
knownLong = float(input("What is the Longitude for the known upper left corner of print {} :".format(knownMap)))
width = int(input("How wide (in feet) is each print: "))
length = int(input("How long (in feet) is each print: "))
knownRow = int(knownMap[0:2])
knownCol = int(knownMap[2:4])

colStepsToZero = (knownCol-startCol) / stepCol
rowStepsToZero = (endRow-knownRow) / stepRow
print(colStepsToZero)
print(rowStepsToZero)

colFtToZero = int(colStepsToZero) * width
rowFtToZero = int(rowStepsToZero) * length

print(colFtToZero)
print(rowFtToZero)
originArray = LatLongMath.FindOrigin([knownLong, knownLat], rowFtToZero, colFtToZero)

print(originArray)

# Create a list of what each X and Y Value label could be
rowValues = list(range(startRow, endRow+stepRow, stepRow))
colValues = list(range(startCol, endCol+stepCol, stepCol))
rowValues.reverse()

mapGrid = LatLongMath.generateGridMatrix(originArray, len(rowValues), len(colValues), length, width)

# Build a dictionary of Row/Columns with the appropriate coordinates
mapDictionary = {}

for R in range(len(rowValues)):
    for C in range(len(colValues)):
        thisBox = [[mapGrid[R][C], 
                   mapGrid[R][C+1],
                   mapGrid[R+1][C+1],
                   mapGrid[R+1][C],
                   mapGrid[R][C]]]
        mapDictionary[repr(rowValues[R])+repr(colValues[C])] = thisBox

print(len(mapDictionary))
sorted(mapDictionary.keys())

geoJsonFeatures = []
for k, v in mapDictionary.items():
    thisPolygon = geojson.Polygon(v)
    thisFeature = geojson.Feature(geometry=thisPolygon, id=k)
    geoJsonFeatures.append(thisFeature)

geoJsonComplete = geojson.FeatureCollection(geoJsonFeatures)

validation = geojson.is_valid(geoJsonComplete)

print(validation['valid'])
print(validation['message'])

print("Writing File")
f = open("GeoJsonOutput", "w")
geojson.dump(geoJsonComplete, f)
f.close()

'''
# This creates a list of X and Y Values
for X in XValues:
    for Y in YValues:
        print(repr(X)+repr(Y))
'''
'''
# Nicer Output of above
output = ""
mapLabels = []
for R in rowValues:
    for C in colValues:
        mapLabels.append(repr(R)+repr(C))
        output += (repr(R)+repr(C))
        output += " "
    output += "\n"

print(output)
print(len(mapLabels))
print(mapLabels.count(str(knownMap)))
'''
