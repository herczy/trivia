import unittest
import sys
import os.path
import StringIO

etalons = {
    'sequential': '''\
Chet was added
They are player number 1
Pat was added
They are player number 2
Sue was added
They are player number 3
Chet is the current player
They have rolled a 1
Chet's new location is 1
The category is Science
Science Question 0
Answer was corrent!!!!
Chet now has 1 Gold Coins.
Pat is the current player
They have rolled a 3
Pat's new location is 3
The category is Rock
Rock Question 0
Answer was corrent!!!!
Pat now has 1 Gold Coins.
Sue is the current player
They have rolled a 5
Sue's new location is 5
The category is Science
Science Question 1
Answer was corrent!!!!
Sue now has 1 Gold Coins.
Chet is the current player
They have rolled a 2
Chet's new location is 3
The category is Rock
Rock Question 1
Question was incorrectly answered
Chet was sent to the penalty box
Pat is the current player
They have rolled a 4
Pat's new location is 7
The category is Rock
Rock Question 2
Answer was corrent!!!!
Pat now has 2 Gold Coins.
Sue is the current player
They have rolled a 1
Sue's new location is 6
The category is Sports
Sports Question 0
Answer was corrent!!!!
Sue now has 2 Gold Coins.
Chet is the current player
They have rolled a 3
Chet is getting out of the penalty box
Chet's new location is 6
The category is Sports
Sports Question 1
Answer was correct!!!!
Chet now has 2 Gold Coins.
Pat is the current player
They have rolled a 5
Pat's new location is 0
The category is Pop
Pop Question 0
Answer was corrent!!!!
Pat now has 3 Gold Coins.
Sue is the current player
They have rolled a 2
Sue's new location is 8
The category is Pop
Pop Question 1
Question was incorrectly answered
Sue was sent to the penalty box
Chet is the current player
They have rolled a 4
Chet is not getting out of the penalty box
Pat is the current player
They have rolled a 1
Pat's new location is 1
The category is Science
Science Question 2
Answer was corrent!!!!
Pat now has 4 Gold Coins.
Sue is the current player
They have rolled a 3
Sue is getting out of the penalty box
Sue's new location is 11
The category is Rock
Rock Question 3
Answer was correct!!!!
Sue now has 3 Gold Coins.
Chet is the current player
They have rolled a 5
Chet is getting out of the penalty box
Chet's new location is 11
The category is Rock
Rock Question 4
Answer was correct!!!!
Chet now has 3 Gold Coins.
Pat is the current player
They have rolled a 2
Pat's new location is 3
The category is Rock
Rock Question 5
Question was incorrectly answered
Pat was sent to the penalty box
Sue is the current player
They have rolled a 4
Sue is not getting out of the penalty box
Chet is the current player
They have rolled a 1
Chet is getting out of the penalty box
Chet's new location is 0
The category is Pop
Pop Question 2
Answer was correct!!!!
Chet now has 4 Gold Coins.
Pat is the current player
They have rolled a 3
Pat is getting out of the penalty box
Pat's new location is 6
The category is Sports
Sports Question 2
Answer was correct!!!!
Pat now has 5 Gold Coins.
Sue is the current player
They have rolled a 5
Sue is getting out of the penalty box
Sue's new location is 4
The category is Pop
Pop Question 3
Answer was correct!!!!
Sue now has 4 Gold Coins.
Chet is the current player
They have rolled a 2
Chet is not getting out of the penalty box
Question was incorrectly answered
Chet was sent to the penalty box
Pat is the current player
They have rolled a 4
Pat is not getting out of the penalty box
Sue is the current player
They have rolled a 1
Sue is getting out of the penalty box
Sue's new location is 5
The category is Science
Science Question 3
Answer was correct!!!!
Sue now has 5 Gold Coins.
Chet is the current player
They have rolled a 3
Chet is getting out of the penalty box
Chet's new location is 3
The category is Rock
Rock Question 6
Answer was correct!!!!
Chet now has 5 Gold Coins.
Pat is the current player
They have rolled a 5
Pat is getting out of the penalty box
Pat's new location is 11
The category is Rock
Rock Question 7
Answer was correct!!!!
Pat now has 6 Gold Coins.
''',
  'random': '''\
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
Question was incorrectly answered
Chet was sent to the penalty box
Pat is the current player
They have rolled a 5
Pat's new location is 5
The category is Science
Science Question 0
Answer was corrent!!!!
Pat now has 1 Gold Coins.
Sue is the current player
They have rolled a 3
Sue's new location is 3
The category is Rock
Rock Question 0
Answer was corrent!!!!
Sue now has 1 Gold Coins.
Chet is the current player
They have rolled a 4
Chet is not getting out of the penalty box
Pat is the current player
They have rolled a 3
Pat's new location is 8
The category is Pop
Pop Question 0
Answer was corrent!!!!
Pat now has 2 Gold Coins.
Sue is the current player
They have rolled a 5
Sue's new location is 8
The category is Pop
Pop Question 1
Answer was corrent!!!!
Sue now has 2 Gold Coins.
Chet is the current player
They have rolled a 2
Chet is not getting out of the penalty box
Question was incorrectly answered
Chet was sent to the penalty box
Pat is the current player
They have rolled a 5
Pat's new location is 1
The category is Science
Science Question 1
Answer was corrent!!!!
Pat now has 3 Gold Coins.
Sue is the current player
They have rolled a 3
Sue's new location is 11
The category is Rock
Rock Question 1
Answer was corrent!!!!
Sue now has 3 Gold Coins.
Chet is the current player
They have rolled a 4
Chet is not getting out of the penalty box
Pat is the current player
They have rolled a 3
Pat's new location is 4
The category is Pop
Pop Question 2
Answer was corrent!!!!
Pat now has 4 Gold Coins.
Sue is the current player
They have rolled a 5
Sue's new location is 4
The category is Pop
Pop Question 3
Answer was corrent!!!!
Sue now has 4 Gold Coins.
Chet is the current player
They have rolled a 2
Chet is not getting out of the penalty box
Question was incorrectly answered
Chet was sent to the penalty box
Pat is the current player
They have rolled a 5
Pat's new location is 9
The category is Science
Science Question 2
Answer was corrent!!!!
Pat now has 5 Gold Coins.
Sue is the current player
They have rolled a 3
Sue's new location is 7
The category is Rock
Rock Question 2
Answer was corrent!!!!
Sue now has 5 Gold Coins.
Chet is the current player
They have rolled a 4
Chet is not getting out of the penalty box
Pat is the current player
They have rolled a 3
Pat's new location is 0
The category is Pop
Pop Question 4
Answer was corrent!!!!
Pat now has 6 Gold Coins.
'''
}


class MockedRandomModule(object):
    def __init__(self, dataset):
        self.dataset = list(dataset)
        self.pos = 0

    def randrange(self, max_range):
        value = self.dataset[self.pos] % max_range
        self.pos = (self.pos + 1) % len(self.dataset)
        return value


class TestTrivia(unittest.TestCase):
    def __run_trivia_script(self, dataset):
        oldout = sys.stdout
        res = sys.stdout = StringIO.StringIO()
        try:
            with self.__create_random_module_replacement(dataset):
                execfile(os.path.join(os.path.dirname(__file__), 'trivia.py'), {'__name__': '__main__'}, {})

        finally:
            sys.stdout = oldout

        return res.getvalue()

    def __create_random_module_replacement(self, dataset):
        class __context(object):
            def __enter__(self):
                sys.modules['random'] = MockedRandomModule(dataset)

            def __exit__(self, *args):
                del sys.modules['random']

        return __context()

    def test_run_with_sequential(self):
        data = self.__run_trivia_script(list(range(10)))
        self.assertEqual(etalons['sequential'], data)

    def test_run_with_random(self):
        data = self.__run_trivia_script([1, 7, 9, 3, 7, 3, 13, 1, 2, 9, 4, 3])
        self.assertEqual(etalons['random'], data)
