from enum import Enum
from typing import List, Tuple
from unittest import TestCase, main


class TokenName(Enum):
    NAME = "NAME"
    ASSIGN = "ASSIGN"
    OP = "OP"
    NUM = "NUM"


CHAR_TO_TOKEN_NAME_MAP = {
    "+": TokenName.OP,
    "=": TokenName.ASSIGN,
    "*": TokenName.OP,
    "/": TokenName.OP,
    "-": TokenName.OP,
}


class Tokenizer:
    def __init__(self, input_str: str):
        self.pos = 0
        self.input = input_str
        self.cur_char = self.input[self.pos]

    def __iter__(self):
        return self

    def __next__(self):
        token = self.get_next_token()
        if token is None:
            raise StopIteration

        return (token[0].name, token[1])

    def advance(self):
        self.pos += 1
        if self.pos < len(self.input):
            self.cur_char = self.input[self.pos]
        else:
            self.cur_char = None

    def skip_whitespace(self):
        while self.cur_char is not None and self.cur_char.isspace():
            self.advance()

    def parse_num(self):
        result = ""
        while self.cur_char is not None and self.cur_char.isdigit():
            result += self.cur_char
            self.advance()
        return result

    def parse_name(self):
        result = ""
        while self.cur_char is not None and self.cur_char.isalpha():
            result += self.cur_char
            self.advance()
        return result

    def get_next_token(self):
        while self.cur_char is not None:
            if self.cur_char.isspace():
                self.skip_whitespace()
            elif self.cur_char.isdigit():
                return TokenName.NUM, self.parse_num()
            elif self.cur_char.isalpha():
                return TokenName.NAME, self.parse_name()
            elif self.cur_char in CHAR_TO_TOKEN_NAME_MAP:
                token = self.cur_char
                token_type = CHAR_TO_TOKEN_NAME_MAP[token]
                self.advance()
                return token_type, token
            else:
                raise ValueError(f"Invalid character: {self.cur_char}")

        return None


def tokenize(text: str):
    tokenizer = Tokenizer(text)
    return list(tokenizer)


def test_tokenize():
    assert tokenize("spam = x + 34 * 567") == [
        ("NAME", "spam"),
        ("ASSIGN", "="),
        ("NAME", "x"),
        ("OP", "+"),
        ("NUM", "34"),
        ("OP", "*"),
        ("NUM", "567"),
    ]


SPACE = " "


def to_source(tree, node_i=0, code=None):
    if code is None:
        code = []
    if node_i >= len(tree):
        return "".join(code)
    node = tree[node_i]

    if isinstance(node, tuple):
        code.append(to_source(node))
    elif node == "assign":
        code.append(to_source(tree, node_i + 1))
        code.append(" = ")
        code.append(to_source(tree, node_i + 2))
    elif node == "binop":
        code.append(to_source(tree, node_i + 2))
        code.append(" ")
        code.append(to_source(tree, node_i + 1))
        code.append(" ")
        code.append(to_source(tree, node_i + 3))
    elif node == "name" or node == "num":
        code.append(to_source(tree, node_i + 1))
    else:
        code.append(node)

    return "".join(code)


def test_to_source():
    tree = (
        "assign",
        "spam",
        ("binop", "+", ("name", "x"), ("binop", "*", ("num", "34"), ("num", "567"))),
    )
    assert to_source(tree) == "spam = x + 34 * 567"


def simplify_tree(tree, node_i=0, new_tree=None):
    if new_tree is None:
        new_tree = []
    if node_i >= len(tree):
        return tuple(new_tree)  # Convert the list back to a tuple before returning
    node = tree[node_i]
    if isinstance(node, tuple):
        new_tree.append(simplify_tree(node))
    elif node == "assign":
        new_tree.append(node)
        new_tree.extend(simplify_tree(tree, node_i + 1))
        new_tree.extend(simplify_tree(tree, node_i + 2))
    elif node == "binop":
        op = simplify_tree(tree, node_i + 1)
        bin1_tree = simplify_tree(tree, node_i + 2)
        bin2_tree = simplify_tree(tree, node_i + 3)

        if bin1_tree[0][0] == "num" and bin2_tree[0][0] == "num":
            if op[0] == "*":
                new_tree.extend(("num", int(bin1_tree[0][1]) * int(bin2_tree[0][1])))
        else:
            new_tree.append(node)
            new_tree.extend(op)
            new_tree.extend(bin1_tree)
            new_tree.extend(bin2_tree)
    elif node == "name" or node == "num":
        new_tree.append(node)
        new_tree.extend(simplify_tree(tree, node_i + 1))
    else:
        new_tree.append(node)
    return tuple(new_tree)  # Ensure the final output is a tuple if needed


def test_simplify_tree():
    tree = ('assign', 'spam', 
        ('binop', '+', 
                  ('name', 'x'),
                  ('binop', '*', ('num', 34), ('num', 567))))
    simple_tree = simplify_tree(tree)
    print(simple_tree)
    assert simple_tree == \
    ('assign', 'spam', ('binop', '+', ('name', 'x'), ('num', 19278)))

if __name__ == "__main__":
    test_tokenize()
    test_to_source()
    test_simplify_tree()
