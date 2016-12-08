# LatLongMath.py
#
# A collection of methods to support generating coordinate sets for PrintMapTool
# outputs are DMS for use in Google Maps
# Note: GeoJSON uses a Long/Lat Format! All returns are given in Long/Lat format
#
# Assumptions:
# * We try to start in the upper left corner of and then work left to right top to bottom
# * Tool is only going to be used in North West Hemisphere (North America)
#   This means Positive Latitude (North) And negative longitude (West)
#
#
# Conversion Formula:
# http://www.movable-type.co.uk/scripts/latlong.html
#

import math

# Constants
ftToKM = 0.0003048
earthRadius = float(6371) # Per https://en.wikipedia.org/wiki/Earth_radius


def generateGridMatrix(longLat, Rows, Columns, shiftInLong, ShiftinLat):
    """ Generates a matrix Coordinate Arrays for a given number of rows
        and columns. Each point refers to one corner of a given print.

        Assumes a latitude change of 3000 feet and a longitude change of 2000 feet

        Keyword Arguments:
        longLat -- The starting point in long/lat format
        Rows - Number of rows needed
        Columns - Number of columns needed
    """
    # Add one to make sure we account for last row and column values
    Rows += 1
    Columns += 1

    # Initialize the Matrix
    gridOutput = [[0 for x in range(Columns)] for y in range(Rows)] 

    currentRowPoint = longLat
    for R in range(Rows):
        currentColumnPoint = currentRowPoint
        for C in range(Columns):
            gridOutput[R][C] = currentColumnPoint
            #currentColumnPoint = BearingDistance(currentColumnPoint, 90, ShiftinLat)
            currentColumnPoint = rhumbDistance(currentColumnPoint, 90, ShiftinLat)
        #currentRowPoint = BearingDistance(currentRowPoint, 180, shiftInLong)
        currentRowPoint = rhumbDistance(currentRowPoint, 180, shiftInLong)

    return gridOutput


def FindOrigin(longLat, shiftInLong, shiftInLat):
    """Returns a Coordinate Array of the upper left corner of the map
        Uses Bearing Method

    Keyword Arguments:
    longLat -- The starting point in long/lat format
    shiftInLat --  The amount (in feet) to shift the latitude Left
    shiftinLong -- The amount (in feet) to shift the longitude Up
    """

    # Shift Left First
    # leftShift = BearingDistance(longLat, 270, shiftInLat)
    leftShift = rhumbDistance(longLat, 270, shiftInLat)
    print(leftShift)
    # shift Up Second
    #upShift = BearingDistance(leftShift, 0, shiftInLong)
    upShift = rhumbDistance(leftShift, 0, shiftInLong)
    return upShift


def rhumbDistance(longLat, bearing, distance):
    """Returns a Coordinate Array for a given bearing and distance away from
       the given lat and long using a Rhumb Line and Mercator Projection
       derived from http://www.movable-type.co.uk/scripts/latlong.html

    Keyword Arguments:
    longLat -- The starting point in long/lat format
    bearing -- the bearing to move the point (In Degrees)
    distance -- the distance to move the point (In Feet)

    Return:
    Coordinate Array in Long/Lat format
    """
    # Degree to Radian conversions
    radLong = math.radians(longLat[0])
    radLat = math.radians(longLat[1])
    radbear = math.radians(bearing)

    # Calculation Simplification
    kmDistance = distance * ftToKM
    angularDist = kmDistance/earthRadius


    # Projection Calculations
    deltaLat = angularDist * math.cos(radbear);
    endLat = radLat + deltaLat;

    deltaPsi = math.log(math.tan(endLat/2+math.pi/4)/math.tan(radLat/2+math.pi/4))
    if(abs(deltaPsi) > 10**-12):
        q = deltaPsi/deltaPsi
    else:
        q = math.cos(radLat)

    deltaLong = angularDist * math.sin(radbear)/q
    endLong = radLong + deltaLong

    return [math.degrees(endLong), math.degrees(endLat)]



def BearingDistance(longLat, bearing, distance):
    """Returns a Coordinate Array for a given bearing and distance away from
       the given lat and long

    Keyword Arguments:
    longLat -- The starting point in long/lat format
    bearing -- the bearing to move the point (In Degrees)
    distance -- the distance to move the point (In Feet)

    Return:
    Coordinate Array in Long/Lat format
    """

    # Degree to Radian conversions
    radLong = math.radians(longLat[0])
    radLat = math.radians(longLat[1])
    radbear = math.radians(bearing)

    # Calculation Simplification
    kmDistance = distance * ftToKM
    angularDist = kmDistance/earthRadius

    endLat = math.asin(math.sin(radLat) * math.cos(angularDist) + (math.cos(radLat) * math.sin(angularDist) * math.cos(radbear)))
    endLong = radLong + math.atan2(math.sin(radbear)*math.sin(angularDist)*math.cos(radLat), math.cos(angularDist)-math.sin(radLat)*math.sin(endLat))

    return [math.degrees(endLong), math.degrees(endLat)]
