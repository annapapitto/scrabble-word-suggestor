from trie import ScoreTrie
import os
import urllib.request as urlreq
import zipfile

"""Scrabble scores for each letter, and url that responds with SOWPODS words."""
SCORES = {"A": 1, "C": 3, "B": 3, "E": 1, "D": 2, "G": 2, "F": 4, "I": 1,
          "H": 4, "K": 5, "J": 8, "M": 3, "L": 1, "O": 1, "N": 1, "Q": 10,
          "P": 3, "S": 1, "R": 1, "U": 1, "T": 1, "W": 4, "V": 4, "Y": 4,
          "X": 8, "Z": 10}
URL = "http://courses.cms.caltech.edu/cs11/material/advjava/lab1/sowpods.zip"

def get_sowpods(url):
    """Download the SOWPODS file from URL, unzip, and return as list."""
    print("Loading SOWPODS words...")
    zipname = "sowpods.zip"
    filename = "sowpods.txt"
    urlreq.urlretrieve(url, zipname)

    zip_ref = zipfile.ZipFile(zipname, 'r')
    zip_ref.extractall()
    zip_ref.close()

    fp = open(filename)
    sowpods = [ word.strip() for word in fp.readlines() ]
    fp.close()

    os.remove(zipname)
    os.remove(filename)
    return sowpods

def get_rack():
    """Get the current letter rack from standard input."""
    rack = input("Enter rack: ")
    if not rack.isalpha():
        raise ValueError("Rack should contain only letters.")
    return rack.upper()

def get_ranked_words(rack, trie):
    """Get valid words from TRIE that can be formed with the letters in RACK.
    Order by decreasing value, tie-breaking with alphabetical ordering."""
    valid = trie.get_words(rack)
    valid.sort(key=lambda word_and_points:word_and_points[0])
    valid.sort(key=lambda word_and_points:word_and_points[1], reverse=True)
    return valid

def print_ranked_words(rack, trie):
    """Display ranked valid words from TRIE formed with the letters in RACK."""
    ranked = get_ranked_words(rack, trie)
    [ print(word + "," + str(points)) for word, points in ranked ]

def run(trie):
    """Keep accepting user's racks and displaying ranked word choices until
    they exit the suggestor using Ctrl+D or Ctrl+C."""
    while True:
        try:
            rack = get_rack()
            print_ranked_words(rack, trie)
        except ValueError as e:
            print(str(e))
        except (KeyboardInterrupt, EOFError) as e:
            print("\nGood luck!")
            exit()
        except Exception as e:
            print("Something went wrong: " + str(e))
            exit()

sowpods = ScoreTrie(get_sowpods(URL), SCORES)
run(sowpods)
