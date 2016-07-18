# LatLongMath.py
#
# A collection of methods to support generating coordinate sets for PrintMapTool
# outputs are DMS for use in Google Maps
# Note: GeoJOSN Hacks are noted as such
#
# Assumptions:
# * We try to start in the upper left corner of and then work left to right top to bottom
# * Tool is only going to be used in North West Hemisphere (North America)
#   This means Postive Latitude (North) And negative logitude (West)
#
# Converstion Forumla:
# http://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-km-distance
# Another example : http://www.movable-type.co.uk/scripts/latlong.html (Using in test code)
#

import math

# Constants
ftToKM = 0.0003048
kmToLat = (1/110.574)
kmToLong = 111.320  # NOTE: Needs to be 1/(111.320*cos(latitude)) to be accurate
earthRadius = float(6371)


def UserInputPrintCoords():
    """ User Input interface to PrintCoords() for testing
    """
    deltaFTLong = int(input("How many feet in width is each map segment? "))
    deltaFTLat = int(input("How many feet in length is each map segment? "))
    givenLat = float(input("What is your starting Latitude? "))
    givenLong = float(input("What is your starting Longitude? "))

    output = PrintCoords(givenLat, givenLong, deltaFTLong, deltaFTLat)

    print("Top Left corner of box should be")
    print(output[0])
    print("Top Right corner of box Should be")
    print(output[1])
    print("Bottom Left CornLer of Box should be")
    print(output [2])
    print("Bottom Right corner of box should be")
    print(output [3])

def PrintCoords(ulLat, ulLong, width, height):
    """Returns an Array of Coordinate Arrays  that form a box starting at a upper left coordinate of a given size

    Keyword Arguments:
    ulLat -- The Upper Left corner Latitude
    ulLong -- The Upper Left Corner Longitude
    Width -- The width of the map (in Feet)
    Height -- The height of the map (in Feet)
    """
    # convert from Feet to Kilometers
    deltaKMLong = width * ftToKM
    deltaKMLat = round(height * ftToKM,6)

    # Convert from Kilometers to Lat/Long changes
    deltaLong = (1/(kmToLong*math.cos(math.radians(ulLat)))) * deltaKMLong
    deltaLat = deltaKMLat * kmToLat

    # Corner Coordinates, GeoJSON requires Long/Lat Notation
    ulCorner = [ulLong, ulLat]
    urCorner = [(deltaLong+ulLong), ulLat]
    llCorner = [ulLong, (ulLat - deltaLat)]
    lrCorner = [(deltaLong + ulLong), (ulLat - deltaLat)]

    return [ulCorner,urCorner,lrCorner,llCorner,ulCorner] #GeoJSON requires a polygon to end on the same part

def FindOrgin(givenLat,givenLong,shiftInLat,shiftInLong):
    """Returns a Coordinate Array of the upper left corner of the map

    Keyword Arguments:
    givenLat -- The Latitude to start from
    givenLong -- The Longitude to start From
    shiftInLat --  The ammount (in feet) to shift the latitude Left
    shiftinLong -- The ammount (in feet) to shift the longitued Up
    """

    # convert from Feet to Kilometers
    deltaKMLong = shiftInLong * ftToKM
    deltaKMLat = shiftInLat * ftToKM

    # Convert from Kilometers to Lat/Long changes
    deltaLong = (1/(kmToLong*math.cos(math.radians(givenLat)))) * deltaKMLong
    deltaLat = deltaKMLat * kmToLat

    return [givenLong-deltaLong, givenLat+deltaLat] #GeoJSON requires long/lat format


def FindOrginNew(givenLat, givenLong, shiftInLat, shiftInLong):
    """Returns a Coordinate Array of the upper left corner of the map
        Uses Bearing Method

    Keyword Arguments:
    givenLat -- The Latitude to start from
    givenLong -- The Longitude to start From
    shiftInLat --  The ammount (in feet) to shift the latitude Left
    shiftinLong -- The ammount (in feet) to shift the longitued Up
    """

    # Shift Left First
    leftShift = BearingDistanceTest(givenLat, givenLong, 270, shiftInLat)

    # shift Up Second
    upShift = BearingDistanceTest(leftShift[0], leftShift[1] , 0, shiftInLong)

    return upShift # Note: Right now were returning inn Lat/Long format


def BearingDistanceTest(givenLat, givenLong, bearing, distance):
    """Returns a Coordinate Array for a given bearing and distance away from
       the given lat and long

    Keyword Arguments:
    givenLat -- The Latitude to start from
    givenLong -- The Longitude to start From
    bearing -- the bearing to move the point (In Degrees)
    distance -- the distance to move the point (In Feet)
    """

    # Degree to Radian conversions
    radLat = math.radians(givenLat)
    radLong = math.radians(givenLong)
    radbear = math.radians(bearing)

    # Calcuation Simplification
    kmDistance = distance * ftToKM
    angularDist = kmDistance/earthRadius

    lat2 = math.asin(math.sin((radLat) * math.cos(angularDist)) + (math.cos(radLat) * math.sin(angularDist) * math.cos(radbear)))
    long2 = radLong + math.atan2(math.sin(radbear)*math.sin(angularDist)*math.cos(radLat), math.cos(angularDist)-math.sin(radLat)*math.sin(lat2))

    return [math.degrees(lat2), math.degrees(long2)]

print(BearingDistanceTest(32.384696,-86.135105,90,3000))
print(BearingDistanceTest(32.384696,-86.135105,180,2000))
