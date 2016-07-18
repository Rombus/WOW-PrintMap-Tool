# LatLongMath.py
#
# A collection of methods to support generating coordinate sets for PrintMapTool
# outputs are DMS for use in Google Maps
# Note: GeoJSON uses a Long/Lat Format! All returns are given in Long/Lat format
#
# Assumptions:
# * We try to start in the upper left corner of and then work left to right top to bottom
# * Tool is only going to be used in North West Hemisphere (North America)
#   This means Postive Latitude (North) And negative logitude (West)
#
#
# Converstion Forumla:
# http://www.movable-type.co.uk/scripts/latlong.html
#

import math

# Constants
ftToKM = 0.0003048
earthRadius = float(6371) # Per https://en.wikipedia.org/wiki/Earth_radius


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
    """Returns an Array of Coordinate Arrays  that form a box starting
    at a upper left coordinate of a given size

    Keyword Arguments:
    ulLat -- The Upper Left corner Latitude
    ulLong -- The Upper Left Corner Longitude
    Width -- The width of the map (in Feet)
    Height -- The height of the map (in Feet)
    """
    # Corner Coordinates, GeoJSON requires Long/Lat Notation
    ulCorner = [ulLong, ulLat]
    urCorner = [(deltaLong+ulLong), ulLat]
    llCorner = [ulLong, (ulLat - deltaLat)]
    lrCorner = [(deltaLong + ulLong), (ulLat - deltaLat)]

    return [ulCorner,urCorner,lrCorner,llCorner,ulCorner] #GeoJSON requires a polygon to end on the same part


def FindOrgin(givenLat, givenLong, shiftInLat, shiftInLong):
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

    return upShift


def BearingDistance(givenLat, givenLong, bearing, distance):
    """Returns a Coordinate Array for a given bearing and distance away from
       the given lat and long

    Keyword Arguments:
    givenLat -- The Latitude to start from
    givenLong -- The Longitude to start From
    bearing -- the bearing to move the point (In Degrees)
    distance -- the distance to move the point (In Feet)

    Return:
    Coordinate Array in Long/Lat format
    """

    # Degree to Radian conversions
    radLat = math.radians(givenLat)
    radLong = math.radians(givenLong)
    radbear = math.radians(bearing)

    # Calcuation Simplification
    kmDistance = distance * ftToKM
    angularDist = kmDistance/earthRadius

    endLat = math.asin(math.sin((radLat) * math.cos(angularDist)) + (math.cos(radLat) * math.sin(angularDist) * math.cos(radbear)))
    endLong = radLong + math.atan2(math.sin(radbear)*math.sin(angularDist)*math.cos(radLat), math.cos(angularDist)-math.sin(radLat)*math.sin(endLat))

    return [math.degrees(endLong), math.degrees(endLat)]