import os, sys
# Gets a list of print files and performs various actions on them

directory = input("What directory do you want to search for prints in?")

rawlist = os.listdir( directory )

for entry in rawlist:
    print(entry)
