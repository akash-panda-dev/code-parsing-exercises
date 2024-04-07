from typing import Tuple, List
from enum import Enum
from unittest import TestCase, main

class TokenName(Enum):
    NAME = 'NAME'
    ASSIGN = 'ASSIGN'
    OP = 'OP'
    NUM = 'NUM'

CHAR_TO_TOKEN_NAME_MAP = {
    '+': TokenName.OP,
    '=': TokenName.ASSIGN,
    '*': TokenName.OP,
    '/': TokenName.OP,
    '-': TokenName.OP,
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
        ('NAME', 'spam'), ('ASSIGN', '='), ('NAME', 'x'), 
        ('OP', '+'), ('NUM', '34'), ('OP', '*'), ('NUM', '567')
    ]

if __name__=="__main__":
    test_tokenize()