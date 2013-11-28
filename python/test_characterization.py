'''
import unittest
import sys
import os.path
import StringIO

import difflib


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
                execfile(os.path.join(os.path.dirname(__file__), 'trivia.py'), {'__name__': '__main__'})

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
        self.__assert_is_the_same('sequential', data)

    def test_run_with_random(self):
        data = self.__run_trivia_script([1, 7, 9, 3, 7, 3, 13, 1, 2, 9, 4, 3])
        self.__assert_is_the_same('random', data)

    def __assert_is_the_same(self, name, data):
        filename = os.path.join(os.path.dirname(__file__), '{}.game.txt'.format(name))

        with open(filename) as f:
            etalon = f.read()

        try:
            self.assertEqual(etalon, data)

        except AssertionError:
            with open(filename + '.result', 'w') as o:
                o.write(data)

            print ('\n'.join(s.rstrip() for s in difflib.unified_diff(data.split('\n'), etalon.split('\n'))))
            raise
'''
