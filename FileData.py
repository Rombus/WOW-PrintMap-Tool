# FileData.py
#
# A class representing the FileSystem and data that is retrievable from it
#

import os
import re


class FileData(object):
    # Class Variables
    directory = ""
    printList = []
    rowInts = []
    colInts = []
    rowStep = 0
    colStep = 0

    def __init__(self, directory):
        """
        Creates a new FileData object from a given Directory
        Args:
            directory: A file system directory containing prints in a RRCC.dwg format

        Returns: a new FileData object
        """
        self.directory = directory
        rawList = os.listdir(self.directory)
        rows = []
        cols = []
        for entry in rawList:
            matchFile = re.match('[0-9][0-9][0-9][0-9].dwg', entry)
            if matchFile:
                thisMatch = matchFile.group()
                self.printList.append(thisMatch)
                rows.append(int(thisMatch[0:2]))  # Row numbers from print number
                cols.append(int(thisMatch[2:4]))  # Column numbers from print number

        # Duplicate Removal
        rows = set(rows)
        cols = set(cols)

        # back to lists
        for r in rows:
            self.rowInts.append(r)
        for c in cols:
            self.colInts.append(c)

        # get our step counts
        print("row 1 ", self.rowInts[1])
        print("row 0 ", self.rowInts[0])
        print("col 1 ", self.colInts[1])
        print("col 0 ", self.colInts[0])
        self.rowStep = self.rowInts[3] - self.rowInts[2]
        self.colStep = self.colInts[1] - self.colInts[0]



    def colStepsToZero(self, givenCol):
        """
        returns the number of column steps needed to get to the left of the map

        Args:
            givenCol: The starting col

        Returns: Number of steps needed to get to the left of the map in integer form

        """
        return (givenCol - self.minCol()) / self.colStep

    def rowStepsToZero(self, givenRow):
        """
        returns the number of row steps needed to get to the top of the map

        Args:
            givenRow: The starting row

        Returns: Number of steps needed to get to the top of the map in interger form

        """

        return (self.maxRow() - givenRow) / self.rowStep

    def maxRow(self):
        return max(self.rowInts)

    def minRow(self):
        return min(self.rowInts)

    def maxCol(self):
        return max(self.colInts)

    def minCol(self):
        return min(self.colInts)

