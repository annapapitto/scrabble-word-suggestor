import argparse
from trie import ScoreTrie
import os
import urllib.request as urlreq
import zipfile

"""Scrabble scores for each letter."""
scores = {"a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2,
         "f": 4, "i": 1, "h": 4, "k": 5, "j": 8, "m": 3,
         "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
         "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4,
         "x": 8, "z": 10}

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
sowpods = Trie(sowpods)

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

"""Rate the valid words and order by points."""
values = { word: points(word) for word in valid ]

def points(word):
    return sum(scores[letter] for letter in word)

ranking = sorted(zip(values, valid))

"""Print out the ranking, first the number of points, then the word formed."""
[ print(",".join(entry)) for entry in ranking ]
