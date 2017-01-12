import argparse
from trie import ScoreTrie
import os
import urllib.request as urlreq
import zipfile

"""Scrabble scores for each letter."""
scores = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2,
         "F": 4, "I": 1, "H": 4, "K": 5, "J": 8, "M": 3,
         "L": 1, "O": 1, "N": 1, "Q": 10, "P": 3, "S": 1,
         "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4,
         "X": 8, "Z": 10}

"""Download the SOWPODS list and unzip and store in local directory."""
url = "http://courses.cms.caltech.edu/cs11/material/advjava/lab1/sowpods.zip"
zipname = "sowpods.zip"
filename = "sowpods.txt"
urlreq.urlretrieve(url, zipname)

zip_ref = zipfile.ZipFile(zipname, 'r')
zip_ref.extractall()
zip_ref.close()

"""Make Trie of SOWPODS words from file."""
fp = open(filename)
sowpods = [ word.strip() for word in fp.readlines() ]
fp.close()

print("start tree")
sowpods = ScoreTrie(sowpods, scores)
print("built tree")

"""Cleans up SOWPODS files. Maybe later I should leave and not re-download if possible."""
os.remove(zipname)
os.remove(filename)

"""Get the current letter rack from the command line."""
parser = argparse.ArgumentParser(description="List valid Scrabble words and their scores given a user's rack.")
parser.add_argument('rack', metavar='LETTERS',
                     help="All letters in your scrabble rack")
args = parser.parse_args()

rack = args.rack.upper()
print("The rack is: ", args.rack)

"""Find all the SOWPODS words that can be formed with the player's rack."""
valid = sowpods.get_words(rack)

"""Order by decreasing value, tie-breaking with alphabetical ordering."""
valid.sort(key=lambda word_and_points:word_and_points[0])
valid.sort(key=lambda word_and_points:word_and_points[1], reverse=True)

"""Print out the ranking, first the number of points, then the word formed."""
[ print(word + "," + str(points)) for word, points in valid ]

"""TODO: modularize into different files. Take util functions out of trie. keep prompting for input racks rather than relying on command line once, or allow command line to take multiple racks."""
