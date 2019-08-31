# @see https://github.com/ZhukovAlexander/triegex
import collections

__all__ = ("Triegex",)

OR = r"|"

# regex below matches nothing https://stackoverflow.com/a/940840/2183102. We
# use '~' to ensure it comes last when lexicographically sorted:
# max(string.printable) is '~'
NOTHING = r"~^(?#match nothing)"
GROUP = r"(?:{0})"
WORD_BOUNDARY = r"\b"


class TriegexNode:
    def __init__(self, char: str, end: bool, *children):
        self.char = char if char is not None else ""
        self.end = end
        self.children = {child.char: child for child in children}

    def __iter__(self):
        return iter(sorted(self.children.values(), key=lambda x: x.char))

    def __len__(self):
        return len(self.children)

    def __repr__(self):
        return "<TriegexNode: '{0.char}' end={0.end}>".format(self)

    def __contains__(self, key):
        return key in self.children

    def __getitem__(self, key):
        return self.children[key]

    def __delitem__(self, key):
        del self.children[key]

    def to_regex(self):
        """
        RECURSIVE IMPLEMENTATION FOR REFERENCE
        suffixes = [v.to_regex() for k, v in self.children.items()]
        if self.end:
            suffixes += [WORD_BOUNDARY]

        if len(suffixes) > 1:
            return self.char + GROUP.format(OR.join(suffixes))
        elif len(suffixes) == 1:
            return self.char + suffixes[0]
        else:
            return self.char
        """

        stack = [self]
        # marks starting indices of children of a node
        lookup = []

        # Creates an ordered list of nodes starting with root and ending with leaves by using BFS
        i = 0
        j = 1
        while i < len(stack):
            stack.extend(sorted(stack[i].children.values(), key=lambda node: node.char))
            lookup.append(j)
            j += len(stack[i].children)
            i += 1

        i = len(stack)
        # temp value array
        sub_regexes = [None] * i
        while i > 0:
            # We start with leaves and end at root thus we decrement
            i -= 1
            node = stack[i]
            # Get regexes of child nodes and make a root regex
            suffixes = [
                sub_regexes[child] for child in range(lookup[i], lookup[i] + len(node.children))
            ]
            if node.end:
                # if the node is an ending node we add a \b character
                suffixes += [WORD_BOUNDARY]
            # If we arrive at the root node we have to add the NOTHING expression
            if i == 0:
                suffixes += [NOTHING]
            if len(suffixes) > 1:
                sub_regexes[i] = node.char + GROUP.format(OR.join(suffixes))
            elif len(suffixes) == 1:
                sub_regexes[i] = node.char + suffixes[0]
            else:
                sub_regexes[i] = node.char
        # return the top Regex
        return sub_regexes[0]


class Triegex(collections.MutableSet):
    def __init__(self, *words):
        """
        Trigex constructor.
        """

        self._root = TriegexNode(None, False)

        for word in words:
            self.add(word)

    def add(self, word: str):
        current = self._root
        for letter in word[:-1]:
            if letter in current.children:
                current = current.children[letter]
            else:
                current = current.children.setdefault(letter, TriegexNode(letter, False))
        # this will ensure that we correctly match the word boundary
        if word[-1] in current.children:
            current.children[word[-1]].end = True
        else:
            current.children[word[-1]] = TriegexNode(word[-1], True)

    def to_regex(self):
        r"""
            Produce regular expression that will match each word in the
        internal trie.

        >>> t = Triegex('foo', 'bar', 'baz')
        >>> t.to_regex()
        '(?:ba(?:r\\b|z\\b)|foo\\b|~^(?#match nothing))'
        """
        return self._root.to_regex()

    def _traverse(self):
        stack = [self._root]
        current = self._root
        while stack:
            yield current
            current = stack.pop()
            stack.extend(current.children.values())

    def __iter__(self):
        paths = {self._root.char: []}
        for node in self._traverse():
            for child in node:
                paths[child.char] = [node.char] + paths[node.char]
                if child.end:
                    char = child.char
                    yield "".join(reversed([char] + paths[char]))

    def __len__(self):
        return sum(1 for _ in self.__iter__())

    def __contains__(self, word):
        current = self._root
        for char in word:
            if char not in current:
                return False
            current = current[char]
        return True and current.end  # word has to end with the last char

    def discard(self, word):
        to_delete = [self._root]
        current = self._root
        for char in word:
            if char not in current:
                return
            current = current[char]
            to_delete.append(current)
        if not to_delete[-1].end:
            return
        while len(to_delete) > 1:
            node = to_delete.pop()
            if len(node) == 0:
                del to_delete[-1][node.char]
            return
