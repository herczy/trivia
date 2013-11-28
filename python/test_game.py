import unittest
from trivia import Game, Player, Question, QuestionSet, InternationalizedGame
import gettext
import mock
import sys
import StringIO


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


class TestQuestionSet(unittest.TestCase):
    def setUp(self):
        self.questions = QuestionSet(('a', 'b'))
        self.player = Player('x')

    def test_initialize(self):
        self.assertEqual(['a', 'b'], self.questions.categories)

    def test_get_next_question(self):
        self.assertEqual('a Question 0', self.questions.get_next_question(self.player).description)

    def test_get_next_question_twice(self):
        self.assertEqual('a Question 0', self.questions.get_next_question(self.player).description)
        self.assertEqual('a Question 1', self.questions.get_next_question(self.player).description)

    def test_get_category(self):
        self.assertEqual('a', self.questions.get_category(self.player))

        self.player.place += 3
        self.assertEqual('b', self.questions.get_category(self.player))


class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = FakeGame()
        self.game.add('player1')
        self.game.add('player2')

        self.one_player_game = FakeGame()
        self.one_player_game.add('player1')

    def test_add(self):
        self.assertEqual([Player('player1'), Player('player2')], list(self.game.players))

    def test_current_player(self):
        self.assertEqual(Player('player1'), self.game.current_player)

    def test_set_next_player_with_one_player(self):
        self.one_player_game.set_next_player()

        self.assertEqual(Player('player1'), self.game.current_player)

    def test_set_next_player_with_two_player(self):
        self.game.set_next_player()

        self.assertEqual(Player('player2'), self.game.current_player)

    def test_not_playable_with_one_player(self):
        self.assertFalse(self.one_player_game.is_playable())

    def test_playable_with_two_player(self):
        self.assertTrue(self.game.is_playable())

    def test_wrong_answer(self):
        self.game.wrong_answer()

        self.assertEqual(Player('player2'), self.game.current_player)

    def test_was_correct_for_the_first_question(self):
        self.assertTrue(self.game.was_correctly_answered())
        self.assertEqual(Player('player2'), self.game.current_player)
        self.assertEqual(1, self.game.players[0].purse)

    def test_was_correct_for_a_penaltied_player(self):
        self.game.current_player.in_penalty_box = True

        self.assertTrue(self.game.was_correctly_answered())
        self.assertEqual(Player('player2'), self.game.current_player)
        self.assertEqual(0, self.game.players[0].purse)


class FakeGame(Game):
    def __init__(self):
        self.messages = []
        super(FakeGame, self).__init__()

    def _report(self, msg, *args, **kwargs):
        self.messages.append((msg, args, kwargs))


class TestInternationalizedGame(unittest.TestCase):
    @mock.patch('trivia.gettext')
    def test_translated(self, gettext):
        gettext.return_value = 'blabla'

        oldout = sys.stdout
        res = sys.stdout = StringIO.StringIO()
        try:
            InternationalizedGame()._report('albalb')

        finally:
            sys.stdout = oldout

        self.assertEqual('blabla\n', res.getvalue())
