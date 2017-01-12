import itertools

class Node():
    def __init__(self, val):
        self.val = val
        self.children = []

    def get_child(self, val):
        for c in self.children:
            if c.val == val:
                return c

    def has_child(self, test):
        return test in [ c.val for c in self.children ]

    def add_child(self, val):
        self.children.append(Node(val))

    def get_word_and_score(self):
        for c in self.children:
            if not isinstance(c.val, str):
                return c.val

class ScoreTrie():
    def __init__(self, words, scores):
        self.scores = scores
        self.root = Node("")
        self.make_trie(words)

    def get_score(self, letter):
        return self.scores[letter]

    def make_trie(self, words):
        [ self.put(word) for word in words ]

    def put(self, word):
        points = 0
        curr_node = self.root
        for letter in word:
            points += self.get_score(letter)
            if not curr_node.has_child(letter):
                curr_node.add_child(letter)
            curr_node = curr_node.get_child(letter)
        #now at node of last letter, want to point to leaf with score in
        curr_node.add_child( (word, points) )

    def get_words(self, letters):
        all_orders = itertools.permutations(letters)
        words = []
        [ words.extend(self.get_words_ordered(order)) for order in all_orders ]
        return words

    def get_words_ordered(self, letters):
        words = []
        curr_node = self.root
        for letter in letters:
            if not curr_node.has_child(letter):
                return words
            curr_node = curr_node.get_child(letter)

            word_and_score = curr_node.get_word_and_score()
            if word_and_score:
                words.append(word_and_score)

        return words
