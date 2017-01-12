import itertools

class Node():
    def __init__(self, val):
        self.val = val
        self.children = []
        self.words = []

    def get_child(self, val):
        for c in self.children:
            if c.val == val:
                return c

    def has_child(self, test):
        return test in [ c.val for c in self.children ]

    def add_child(self, val):
        self.children.append(Node(val))

    def get_words(self):
        return self.words[:]

    def add_word(self, word_and_points):
        self.words.append(word_and_points)

class ScoreTrie():
    def __init__(self, words, scores):
        self.scores = scores
        self.root = Node("root")
        self.make_trie(words)

    def get_score(self, letter):
        return self.scores[letter]

    def make_trie(self, words):
        [ self.put(word) for word in words ]

    def put(self, word):
        points = 0
        curr_node = self.root
        for letter in sorted(word):
            points += self.get_score(letter)
            if not curr_node.has_child(letter):
                curr_node.add_child(letter)
            curr_node = curr_node.get_child(letter)
        #now at node of last letter, want to record word exists with score
        curr_node.add_word( (word, points) )

    def get_words(self, letters):
        return self.get_words_ordered(self.root, sorted(letters))

    def get_words_ordered(self, curr_node, letters):
        if not curr_node:
            return []

        if not letters:
            return curr_node.get_words()

        res = []
        use = self.get_words_ordered(curr_node.get_child(letters[0]), letters[1:])
        res.extend(use)
        dont_use = self.get_words_ordered(curr_node, self.skip_letter(letters))
        res.extend(dont_use)
        return res

    def skip_letter(self, letters):
        to_skip = letters[0]
        for i in range(len(letters)):
            if letters[i] != to_skip:
                return letters[i:]
        return ""
