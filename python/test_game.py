'''
Created on Nov 28, 2013

@author: herczy
'''
import unittest
from trivia import Game, Player, Question


class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player('player')

    def test_initialize(self):
        self.assertEqual('player', self.player.name)
        self.assertEqual(0, self.player.place)
        self.assertEqual(0, self.player.purse)
        self.assertFalse(self.player.in_penalty_box)
        self.assertTrue(self.player.has_joker)

    def test_move_to_new_place(self):
        self.player.move_to_new_place(16)

        self.assertEqual(4, self.player.place)

    def test_pay(self):
        self.player.pay()

        self.assertEqual(1, self.player.purse)

    def test_use_joker(self):
        self.player.use_joker()

        self.assertFalse(self.player.has_joker)

    def test_use_nonexistent_joker(self):
        self.player.use_joker()

        self.assertRaises(RuntimeError, self.player.use_joker)

    def test_ask_use_joker(self):
        self.assertFalse(self.player.ask_use_joker(4))
        self.assertTrue(self.player.ask_use_joker(5))
        self.assertFalse(self.player.ask_use_joker(10))


class TestQuestion(unittest.TestCase):
    def setUp(self):
        self.question = Question('Pop', 5)

    def test_initialize(self):
        self.assertEqual('Pop', self.question.category)
        self.assertEqual(5, self.question.ident)

    def test_description(self):
        self.assertEqual('Pop Question 5', self.question.description)

    def test_next_question(self):
        self.assertEqual(6, self.question.get_next_question().ident)


class TestGame(unittest.TestCase):
    def test_add(self):
        game = Game()
        game.add('player1')

        self.assertEqual([Player('player1')], list(game.players))
