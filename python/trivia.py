#!/usr/bin/env python

class Player(object):
    def __init__(self, name):
        self.name = name
        self.place = 0
        self.purse = 0
        self.in_penalty_box = False
        self.has_joker = True

    def __eq__(self, other):
        return self.name == other.name

    def move_to_new_place(self, diff):
        self.place += diff
        if self.place > 11:
            self.place = self.place - 12

    def pay(self):
        self.purse += 1

    def use_joker(self):
        if not self.has_joker:
            raise RuntimeError('no jokers left')

        self.has_joker = False

    def ask_use_joker(self, roll):
        return roll == 5


class Question(object):
    def __init__(self, category, ident):
        self.category = category
        self.ident = ident

    @property
    def description(self):
        return '{} Question {}'.format(self.category, self.ident)

    def get_next_question(self):
        return self.__class__(self.category, self.ident + 1)


class Game(object):
    __categories = ['Pop', 'Science', 'Sports', 'Rock']

    def __init__(self):
        self.players = []

        self.__current_player = 0
        self.is_getting_out_of_penalty_box = False

        self.questions = [Question(category, 0) for category in self.__categories]

    def set_next_player(self):
        self.__current_player += 1
        if self.__current_player == len(self.players):
            self.__current_player = 0

    @property
    def current_player(self):
        return self.players[self.__current_player]

    def is_playable(self):
        return self.how_many_players >= 2

    def add(self, player_name):
        self.players.append(Player(player_name))

        self._report(player_name + " was added")
        self._report("They are player number %s" % len(self.players))

        return True

    @property
    def how_many_players(self):
        return len(self.players)


    def __move_out_of_penalty_box(self, roll):
        self.is_getting_out_of_penalty_box = True
        self._report("%s is getting out of the penalty box" % self.current_player.name)
        self.__ask_new_question(roll)

    def __ask_new_question(self, roll):
        self.current_player.move_to_new_place(roll)
        self._report(self.current_player.name + '\'s new location is ' + str(self.current_player.place))
        self._report("The category is %s" % self._current_category)

        self._ask_question()

    def roll(self, roll):
        self._report("%s is the current player" % self.current_player.name)
        self._report("They have rolled a %s" % roll)

        if self.current_player.in_penalty_box:
            if roll % 2 != 0:
                self.__move_out_of_penalty_box(roll)

            else:
                self._report("%s is not getting out of the penalty box" % self.current_player.name)
                self.is_getting_out_of_penalty_box = False
        else:
            self.__ask_new_question(roll)

    def _ask_question(self):
        index = self.__categories.index(self._current_category)
        res = self.questions[index]
        self.questions[index] = res.get_next_question()
        self._report(res.description)

    @property
    def _current_category(self):
        if self.current_player.place > 10:
            return 'Rock'

        return self.__categories[self.current_player.place % 4]


    def __answer_was_correct(self):
        self._report("Answer was correct!!!!")
        self.current_player.pay()

        self._report(self.current_player.name + ' now has ' + str(self.current_player.purse) + ' Gold Coins.')
        winner = self._did_player_win()
        self.set_next_player()
        return winner

    def was_correctly_answered(self):
        if self.current_player.in_penalty_box:
            if self.is_getting_out_of_penalty_box:
                return self.__answer_was_correct()

            self.set_next_player()
            return True

        return self.__answer_was_correct()

    def wrong_answer(self):
        self._report('Question was incorrectly answered')
        self._report(self.current_player.name + " was sent to the penalty box")
        self.current_player.in_penalty_box = True

        self.set_next_player()
        return True

    def _did_player_win(self):
        return not (self.current_player.purse == 6)

    def _report(self, message):
        print message


from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    while True:
        game.roll(randrange(5) + 1)

        if randrange(9) == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break
