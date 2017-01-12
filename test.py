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
    c.add_child(("ac", 5))
    assert not c.has_child("ac")
    assert c.get_word_and_score() == ("ac", 5)

def points(word, scores):
    return sum([ scores[letter] for letter in word ])


def test_trie():
    scores = { "a": 1, "g": 2, "p": 3 }
    words = [ "a", "pga", "pg", "gpa", "aapga", "ppgg" ]
    ps = { word: points(word, scores) for word in words }

    t = ScoreTrie(words, scores)
    assert t.get_score("g") == 2

    first = t.root.children[0]
    assert first.val == "a"
    assert len(first.children) == 2
    firstfirst = first.children[0]
    assert firstfirst.val == ("a", ps["a"])
    assert first.get_word_and_score() == ("a", ps["a"])

    assert t.get_words("a") == [ ("a", ps["a"]) ]
    assert t.get_words("g") == [ ]
    assert t.get_words("gp") == [ ("pg", ps["pg"]) ]
    assert t.get_words("ga") == [ ("a", ps["a"]) ]

    assert sorted(t.get_words("pgaaa")) == \
        sorted([ ("a", ps["a"]), ("pga", ps["pga"]), ("pg", ps["pg"]),
                 ("gpa", ps["gpa"]), ("aapga", ps["aapga"]) ])

    assert sorted(t.get_words("pppggg")) == \
        sorted([ ("pg", ps["pg"]), ("ppgg", ps["ppgg"]) ])

def test():
    test_node()
    test_trie()






test()
