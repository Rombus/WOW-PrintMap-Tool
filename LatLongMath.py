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

def generateGridMatrix(givenLong, givenLat, Rows, Columns):
    """ Generates a matrix Coordinate Arrays for a given number of rows
        and columns. Each point refers to one corner of a given print.

        Assumes a latitude change of 3000 feet and a longitude change of 2000 feet

        Keyword Arguments:
        givenLong - the longituded to start the grid at (Upper Left Corner)
        givenLat - The latitude to start the grid at (Upper Left Corner)
        Rows - Number of rows needed
        Columns - Number of columns needed
    """

    # Initzalize the Matrix
    gridOutput = [[0 for x in range(Columns + 1)] for y in range(Rows + 1)] 

    currentRowPoint = [givenLong, givenLat]
    for R in Rows:
        currentColumnPoint = currentRowPoint
        for C in Columns:
            gridOutput[R][C] = currentColumnPoint
            currentColumnPoint = BearingDistance(currentColumnPoint[1], currentColumnPoint[0], 90, 3000)
        currentRowPoint = BearingDistance(currentRowPoint[1], currentRowPoint[0], 180, 2000)

    return gridOutput


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
    leftShift = BearingDistance(givenLat, givenLong, 270, shiftInLat)

    # shift Up Second
    upShift = BearingDistance(leftShift[0], leftShift[1] , 0, shiftInLong)

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
