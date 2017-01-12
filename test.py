from trie import Node, ScoreTrie

"""Testing trie implementation."""
def test_node():
    n = Node("a")
    assert not n.has_child("b")
    n.add_child("b")
    assert n.has_child("b")
    n.add_child("c")
    assert n.has_child("b")
    assert n.has_child("c")

    c = n.get_child("c")
    assert c.val == "c"
    c.add_word(("ac", 5))
    assert not c.has_child("ac")
    assert c.get_words() == [ ("ac", 5) ]

def points(word, scores):
    return sum([ scores[letter] for letter in word ])


def test_trie():
    scores = { "a": 1, "g": 2, "p": 3 }
    words = [ "a", "pga", "pg", "gpa", "aapga", "pggp" ]
    ps = { word: points(word, scores) for word in words }

    t = ScoreTrie(words, scores)
    assert t.get_score("g") == 2

    first = t.root.children[0]
    assert first.val == "a"
    assert len(first.children) == 2
    assert first.get_words() == [ ("a", ps["a"]) ]

    assert t.get_words("a") == [ ("a", ps["a"]) ]
    assert t.get_words("g") == [ ]
    assert t.get_words("gp") == [ ("pg", ps["pg"]) ]
    assert t.get_words("ga") == [ ("a", ps["a"]) ]

    assert sorted(t.get_words("apg")) == \
        sorted([ ("a", ps["a"]), ("pga", ps["pga"]),
                 ("pg", ps["pg"]), ("gpa", ps["gpa"]) ])

    assert t.skip_letter("aaapg") == "pg"

    assert sorted(t.get_words("pgaaa")) == \
        sorted([ ("a", ps["a"]), ("pga", ps["pga"]), ("pg", ps["pg"]),
                 ("gpa", ps["gpa"]), ("aapga", ps["aapga"]) ])

    assert sorted(t.get_words("pppggg")) == \
        sorted([ ("pg", ps["pg"]), ("pggp", ps["pggp"]) ])

    assert t.get_words("") == [ ]
    t2 = ScoreTrie([], scores)
    assert t2.get_words("abc") == [ ]

def test():
    test_node()
    test_trie()






test()
