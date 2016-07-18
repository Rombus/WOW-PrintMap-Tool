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
stepCol = int(input ("how many steps between each column: "))
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

print(length)
print(width)
colFtToZero = int(colStepsToZero) * width
rowFtToZero = int(rowStepsToZero) * length

print(colFtToZero)
print(rowFtToZero)
orginArray = LatLongMath.FindOrgin(knownLat, knownLong, rowFtToZero, colFtToZero)

print(orginArray)

# Create a list of what each X and Y Value label could be
rowValues = list(range(startRow,endRow+1,stepRow))
colValues = list(range(startCol,endCol+1,stepCol))
rowValues.reverse()

# Build a dictionary of Row/Columns with the approprate coordinates
mapDictionary = {}
nextRowStart = orginArray # Start with the orginArray we figured out earlier)
nextBoxStart = [] # This contains the uper left of th next box
newRowFlag = False

for R in rowValues:
    newRowFlag = True
    nextBoxStart = nextRowStart
    for C in colValues:
        thisBox = LatLongMath.PrintCoords(nextBoxStart[0], nextBoxStart[1], width, length)
        nextBoxStart = thisBox[1] # This should be the upper right corner of the given box
        if newRowFlag:
            nextRowStart = thisBox[2] # this should be the lower right corner of the given box
            newRowFlag = False
        mapDictionary[(repr(R)+repr(C))] = thisBox

print(len(mapDictionary))
sorted(mapDictionary.keys())

geoJsonFeatures=[]
for k, v i26n mapDictionary.items():
    thisPolygon = geojson.Polygon(v)
    thisFeature = geojson.Feature(geometry = thisPolygon, id = k)
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
