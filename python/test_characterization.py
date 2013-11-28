import unittest
import sys
import os.path
import StringIO

etalons = {
    'run': '''\
Chet was added
They are player number 1
Pat was added
They are player number 2
Sue was added
They are player number 3
Chet is the current player
They have rolled a 2
Chet's new location is 2
The category is Sports
Sports Question 0
Answer was corrent!!!!
Chet now has 1 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 2
The category is Sports
Sports Question 1
Answer was corrent!!!!
Pat now has 1 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 2
The category is Sports
Sports Question 2
Answer was corrent!!!!
Sue now has 1 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 4
The category is Pop
Pop Question 0
Answer was corrent!!!!
Chet now has 2 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 4
The category is Pop
Pop Question 1
Answer was corrent!!!!
Pat now has 2 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 4
The category is Pop
Pop Question 2
Answer was corrent!!!!
Sue now has 2 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 6
The category is Sports
Sports Question 3
Answer was corrent!!!!
Chet now has 3 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 6
The category is Sports
Sports Question 4
Answer was corrent!!!!
Pat now has 3 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 6
The category is Sports
Sports Question 5
Answer was corrent!!!!
Sue now has 3 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 8
The category is Pop
Pop Question 3
Answer was corrent!!!!
Chet now has 4 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 8
The category is Pop
Pop Question 4
Answer was corrent!!!!
Pat now has 4 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 8
The category is Pop
Pop Question 5
Answer was corrent!!!!
Sue now has 4 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 10
The category is Sports
Sports Question 6
Answer was corrent!!!!
Chet now has 5 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 10
The category is Sports
Sports Question 7
Answer was corrent!!!!
Pat now has 5 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 10
The category is Sports
Sports Question 8
Answer was corrent!!!!
Sue now has 5 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 0
The category is Pop
Pop Question 6
Answer was corrent!!!!
Chet now has 6 Gold Coins.
'''
}


class MockedRandomModule(object):
    def __init__(self):
        self.dataset = [i for i in range(10)]
        self.pos = 0

    def randrange(self, max_range):
        value = self.dataset[self.pos + 1] % max_range
        self.pos = self.pos % len(self.dataset)
        return value


class TestTrivia(unittest.TestCase):
    def setUp(self):
        self.random = MockedRandomModule()
        sys.modules['random'] = self.random

    def __run_trivia_script(self):
        oldout = sys.stdout
        res = sys.stdout = StringIO.StringIO()
        try:
            execfile(os.path.join(os.path.dirname(__file__), 'trivia.py'), {'__name__': '__main__'})

        finally:
            sys.stdout = oldout

        return res.getvalue()

    def test_run(self):
        self.assertEqual(etalons['run'], self.__run_trivia_script())
