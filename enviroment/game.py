from random import shuffle
import random
import queue
import fileinput
from colorama import init
from termcolor import colored
from PIL import ImageTk, Image

TOP_HAND_SCORE = {'66': 1, '77': 2, '88': 3, '99': 4, '1010': 5, '1111': 6, '1212': 7, '1313': 8, '11': 9,
                  '222': 10, '333': 11, '444': 12, '555': 13, '666': 14, '777': 15, '888': 16, '999': 17,
                  '101010': 18, '111111': 19, '121212': 20, '131313': 21, '111': 22}
MID_HAND_SCORE = {'high': 0, 'pair': 0, 'two_pair': 0, 'trips': 2, 'straight': 4, 'flush': 8, 'full_house': 12,
                  'quads': 20,
                  'poker': 30, 'royal': 50}
BOTTOM_HAND_SCORE = {'high': 0, 'pair': 0, 'two_pair': 0, 'straight': 2, 'flush': 4, 'full_house': 6, 'quads': 10,
                     'poker': 15, 'royal': 25}
HAND_SCORE = [0, TOP_HAND_SCORE, MID_HAND_SCORE, BOTTOM_HAND_SCORE]


# Hand strength
# High
# One pair
# Two Pair
# Trips
# Straight
# Flush
# Full
# Quads
# Straight flush

class Card(object):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.image = None

    def __str__(self):
        return f'{self.value}{self.suit}'

    def __eq__(self, other):
        '''if self.value == other.value and self.suit == other.suit:
            return True
        else:
            False'''
        if self.__str__() == other:
            return True
        return False

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit

    def representation(self):
        self.image = ImageTk.PhotoImage(Image.open("Cards/{}{}.png".format(self.value, self.suit)))
        return self.image


class Deck(object):
    def __init__(self, random_seed, burnt_cards=None):
        self.cards = []
        self.random_seed = random_seed
        self.burn_cards = burnt_cards
        self.build()

    def build(self):
        suits = ['S', 'C', 'H', 'D']
        deck_of_cards = []
        for rank in range(2, 15):
            for suit in suits:
                deck_of_cards.append(Card(rank, suit))
        if isinstance(self.burn_cards, list):
            [deck_of_cards.remove(card) for card in self.burn_cards]
        random.seed(self.random_seed)
        shuffle(deck_of_cards)
        q2 = queue.Queue()
        q2.queue = queue.deque(deck_of_cards)
        self.cards = q2

    def get_card(self):
        return self.cards.queue.pop()


# class HandStrength(object):
#     # need to be implemented in hand
#     def __init__(self, cards):
#         self.hand_type = 0
#         self.hand_name = ''
#         self.ranks = [v.get_value() for v in cards]
#         self.suit = [v.get_suit() for v in cards]
#         self.to_compare = []
#         self.points = 0
#         # made hand evaluation
#         histogram = {}
#         ranks = self.ranks
#         ranks.sort()
#         if len(ranks) == 5:
#             for r in ranks:
#                 if r in histogram.keys():
#                     histogram[r] = histogram[r] + 1
#                 else:
#                     histogram[r] = 1
#             hist_values = histogram.values()
#             hand_type = {0: 'high', 1: 'pair', 2: 'two_pair', 3: 'trips', 4: 'straight', 5: 'flush', 6: 'full',
#                          7: 'quads', 8: 'poker'}
#             if max(hist_values) == 4:
#                 # quads
#                 self.hand_id = 7
#                 self.hand_name = hand_type[self.hand_id]
#                 for rank, quantity in histogram.items():
#                     if quantity == 4:
#                         self.to_compare = [rank]
#             elif len(hist_values) == 2:
#                 # full
#                 self.hand_id = 6
#                 self.hand_name = hand_type[self.hand_id]
#                 for rank, quantity in histogram.items():
#                     if quantity == 2:
#                         pair = rank
#                     else:
#                         trips = rank
#                 self.to_compare = [trips, pair]
#             elif max(hist_values) == 3:
#                 # trips
#                 self.hand_id = 3
#                 self.hand_name = hand_type[self.hand_id]
#                 for rank, quantity in histogram.items():
#                     if quantity == 3:
#                         self.to_compare.append(rank)
#                 # TODO be careful with sorting rank without sorting suits
#                 self.to_compare.sort()
#
#             elif len(hist_values) == 3:
#                 # two pairs
#                 self.hand_id = 2
#                 for rank, quantity in histogram.items():
#                     if quantity == 2:
#                         self.to_compare.append(rank)
#                 # TODO be careful with sorting rank without sorting suits
#                 self.to_compare.sort()
#
#             elif len(hist_values) == 4:
#                 # one pair
#                 self.hand_id = 1
#                 for rank, quantity in histogram.items():
#                     if quantity == 2:
#                         self.to_compare.append(rank)
#             elif set(self.suit) == 1:
#                 # self.ranks.sort()
#                 if ranks[-1] - ranks[0] == 4:
#                     self.hand_type = 'straight_flush'
#                 else:
#                     self.hand_type = 'flush'
#             elif int(ranks[-1]) - int(ranks[0]) == 4:
#                 self.hand_type = 'straight'
#         else:
#             if len(ranks) == 3 and len(set(ranks)) == 1:
#                 hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value(), ranks[2].get_value()])
#             else:
#                 if ranks[0] == ranks[1]:
#                     hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value()])
#                 elif ranks[0] == ranks[2]:
#                     hand_str = ''.join([ranks[0].get_value(), ranks[2].get_value()])
#                 else:
#                     hand_str = ''.join([ranks[1].get_value(), ranks[2].get_value()])
#                 print(f'Hand representation {hand_str}')
#             self.ev = top_hand_royalties[hand_str]
#
#     def __gt__(self, other):
#         if self.hand_id > other.hand_id:
#             return True
#         elif self.hand_id == other.hand_id:
#             for left, right in zip(self.to_compare, other.to_compare):
#                 if left != right:
#                     if left > right:
#                         return True
#                     else:
#                         return False
#                 else:
#                     return
#         else:
#             return False
#


# class FrontHand(object):
#     def __init__(self):
#         self.hand = []
#         self.ev = 0
#         self.royalty = 0
#         self.hand_completed = False
#
#     def evaluate(self):
#         ranks = [v for v in self.hand]
#         if len(ranks) > 1 and len(set(ranks)) < len(ranks):
#             if len(ranks) == 3 and len(set(ranks)) == 1:
#                 hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value(), ranks[2].get_value()])
#             else:
#                 if ranks[0] == ranks[1]:
#                     hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value()])
#                 elif ranks[0] == ranks[2]:
#                     hand_str = ''.join([ranks[0].get_value(), ranks[2].get_value()])
#                 else:
#                     hand_str = ''.join([ranks[1].get_value(), ranks[2].get_value()])
#                 print(f'Hand representation {hand_str}')
#             self.ev = top_hand_royalties[hand_str]
#         else:
#             self.ev = 0.1
#
#     def add_card(self, new_card):
#         if isinstance(new_card, list):
#             for card in new_card:
#                 self.hand.append(card)
#             if len(self.hand) > 3:
#                 self.hand_completed = True
#                 print('To many cards in hand')
#         elif isinstance(new_card, Card):
#             self.hand.append(new_card)

# self.evaluate()
# print(self.ev)

# def hand_strength(self):
#     pass


class FrontMidBotHand(object):
    def __init__(self, max_cards=5, row=None, cards=None):
        self.max_cards = max_cards
        if cards is not None:
            self.hand = cards
        else:
            self.hand = []
        self.temp_hand = []
        self.ev = 0
        self.to_compare = None
        if len(self.hand) < max_cards:
            self.hand_completed = False
        else:
            self.hand_completed = True
        self.hand_name = ''
        self.hand_id = 0
        self.row = row
        self.points = 0

    def evaluate(self):
        self.hand_name = ''
        ranks = [v.get_value() for v in self.hand]
        suit = [v.get_suit() for v in self.hand]
        self.to_compare = []
        # made hand evaluation
        histogram = {}
        ranks.sort()
        if self.max_cards == 5:
            hand_type = {0: 'high', 1: 'pair', 2: 'two_pair', 3: 'trips', 4: 'straight', 5: 'flush', 6: 'full',
                         7: 'quads', 8: 'poker'}

            if len(ranks) == 5:
                for r in ranks:
                    if r in histogram.keys():
                        histogram[r] = histogram[r] + 1
                    else:
                        histogram[r] = 1
                hist_values = histogram.values()

                if max(hist_values) == 4:
                    # quads
                    self.hand_id = 7
                    for rank, quantity in histogram.items():
                        if quantity == 4:
                            self.to_compare = [rank]
                elif len(hist_values) == 2:
                    # full
                    self.hand_id = 6
                    for rank, quantity in histogram.items():
                        if quantity == 2:
                            pair = rank
                        else:
                            trips = rank
                    self.to_compare = [trips, pair]
                elif max(hist_values) == 3:
                    # trips
                    self.hand_id = 3
                    for rank, quantity in histogram.items():
                        if quantity == 3:
                            self.to_compare.append(rank)
                    # TODO be careful with sorting rank without sorting suits
                    self.to_compare.sort()

                elif len(hist_values) == 3:
                    # two pairs
                    self.hand_id = 2
                    for rank, quantity in histogram.items():
                        if quantity == 2:
                            self.to_compare.append(rank)
                    # TODO be careful with sorting rank without sorting suits
                    self.to_compare.sort()

                elif len(hist_values) == 4:
                    # one pair
                    self.hand_id = 1
                    for rank, quantity in histogram.items():
                        if quantity == 2:
                            self.to_compare.append(rank)
                elif len(set(suit)) == 1:
                    # self.ranks.sort()
                    if ranks[-1] - ranks[0] == 4:
                        self.hand_id = 8
                    else:
                        self.hand_id = 5
                elif int(ranks[-1]) - int(ranks[0]) == 4:
                    self.hand_id = 4
                else:
                    self.hand_id = 0
            self.hand_name = hand_type[self.hand_id]
            self.points = HAND_SCORE[self.row][self.hand_name]
            print(self.points)
        #   return hand_type[self.hand_id]
        elif self.max_cards == 3:
            hand_str = ''
            if len(ranks) == 3 and len(set(ranks)) == 1:
                # Trips
                hand_str = ''.join([str(ranks[0]), str(ranks[1]), str(ranks[2])])
                self.hand_id = 3

            elif len(set(ranks)) == 2:
                # Pair
                if ranks[0] == ranks[1]:
                    hand_str = ''.join([str(ranks[0]), str(ranks[1])])
                    self.to_compare = [ranks[0], ranks[1], ranks[2]]
                elif ranks[0] == ranks[2]:
                    hand_str = ''.join([str(ranks[0]), str(ranks[2])])
                    self.to_compare = [ranks[0], ranks[2], ranks[1]]
                else:
                    hand_str = ''.join([str(ranks[1]), str(ranks[2])])
                    self.to_compare = [ranks[1], ranks[2], ranks[0]]
            else:
                self.to_compare = [ranks]
            try:
                self.points = TOP_HAND_SCORE[hand_str]
            except KeyError:
                self.points = 0
            print(self.points)
        return self.hand_id

    def __gt__(self, other):
        if self.evaluate() > other.evaluate():
            return True
        elif self.hand_id == other.hand_id:
            for left, right in zip(self.to_compare, other.to_compare):
                if left != right:
                    if left > right:
                        return True
                    else:
                        return False
                else:
                    return

        def __eq__(self, other):
            # TODO check if hands are equally strong
            pass

    def add_card(self, new_card):
        if isinstance(new_card, list):
            for card in new_card:
                self.hand.append(card)
        elif isinstance(new_card, Card):
            self.hand.append(new_card)
        if len(self.hand) == self.max_cards:
            self.hand_completed = True

    def add_card_to_temp(self, new_card):
        if isinstance(new_card, list):
            for card in new_card:
                self.temp_hand.append(card)
        elif isinstance(new_card, Card):
            self.temp_hand.append(new_card)
            if len(self.hand) + len(self.temp_hand) == self.max_cards:
                self.hand_completed = True

    def set_temp_to_hand(self):
        self.hand.extend(self.temp_hand)
        self.temp_hand = []

    def reset(self):
        hands_to_return = self.temp_hand
        self.temp_hand = []
        return hands_to_return

    def get_hand_len(self):
        return len(self.hand)


class OfcHand(object):

    def __init__(self, top=None, mid=None, bot=None):
        self.top_row = FrontMidBotHand(max_cards=3, row=1, cards=top)
        self.mid_row = FrontMidBotHand(max_cards=5, row=2, cards=mid)
        self.bottom_row = FrontMidBotHand(max_cards=5, row=3, cards=bot)
        self.total_cards = len(self.top_row.hand) + len(self.mid_row.hand) + len(self.bottom_row.hand)

    def is_it_foul(self):
        if len(self.top_row.hand) == 3 and len(self.mid_row.hand) == 5 and len(self.mid_row.hand) == 5:
            # OFC rules

            if self.bottom_row > self.mid_row > self.top_row:
                return True
            else:
                return False
        else:
            return True

    # if self.bottom_row.hand

    def evaluate(self):
        if not self.is_it_foul():
            ev = 0
            for row, hand in enumerate([self.top_row, self.mid_row, self.bottom_row]):
                ev += HAND_SCORE[row][hand.evaluate()]
            return ev

        else:
            return -10

    def add_card(self, card, row):
        if isinstance(row, str):
            if row == '1':
                if not self.top_row.hand_completed:
                    self.top_row.add_card_to_temp(card)
                    return True
                else:
                    print('Hand is completed')
                    return False
            if row == '2':
                if not self.mid_row.hand_completed:
                    self.mid_row.add_card_to_temp(card)
                    return True
                else:
                    print('Hand is completed')
                    return False
            if row == '3':
                if not self.bottom_row.hand_completed:
                    self.bottom_row.add_card_to_temp(card)
                    return True
                else:
                    print('Hand is completed')
                    return False
        else:
            print('Wrong format of row: should be str 1: top, 2:mid and 3:bot')

    def add_card_to_front(self, card, ):
        if not self.top_row.hand_completed:
            self.top_row.add_card(card)
            return True
        else:
            print('Hand is completed')
            return False

    def add_card_to_mid(self, card):
        if not self.mid_row.hand_completed:
            self.mid_row.add_card(card)
            return True
        else:
            print('Hand is completed')
            return

    def add_card_to_bottom(self, card):
        if not self.bottom_row.hand_completed:
            self.bottom_row.add_card(card)
            return True
        else:
            print('Hand is completed')
            return False

    def reset(self):
        self.top_row.temp_hand = []
        self.mid_row.temp_hand = []
        self.bottom_row.temp_hand = []

    def set_changes(self):
        self.top_row.set_temp_to_hand()
        self.mid_row.set_temp_to_hand()
        self.bottom_row.set_temp_to_hand()
        self.total_cards = self.top_row.get_hand_len() + self.bottom_row.get_hand_len() + self.mid_row.get_hand_len()

    def __str__(self):
        game_look = ''

        # front hand
        top_hand = ''
        list_top_hand = [str(hand) + ' | ' for hand in self.top_row.hand]
        top_hand = top_hand.join(list_top_hand)

        # # front temp hand
        # top_hand_temp = ''
        # list_top_hand_temp = [str(hand) + ' | ' for hand in self.top_row.temp_hand]
        # top_hand_temp = top_hand_temp.join(list_top_hand_temp)
        # top_hand_temp = (Back.LIGHTBLACK_EX, top_hand_temp)

        # mid hand
        mid_hand = ''
        list_mid_hand = [str(hand) + ' | ' for hand in self.mid_row.hand]
        mid_hand = mid_hand.join(list_mid_hand)

        # bottom hand
        bottom_hand = ''
        list_bottom_hand = [str(hand) + ' | ' for hand in self.bottom_row.hand]
        bottom_hand = bottom_hand.join(list_bottom_hand)

        line = '_' * 25
        look = [line, '\n', top_hand, '\n', line, '\n', mid_hand, '\n', line, '\n', bottom_hand, '\n', line]
        game_look = game_look.join(look)
        return game_look

    def print_hand(self):
        # print hand in the terminal
        # Cards placed in current round and can be moved have cyan background
        init()
        # front hand
        top_hand = ''
        list_top_hand = [str(hand) + ' | ' for hand in self.top_row.hand]
        top_hand = top_hand.join(list_top_hand)

        # front temp hand
        top_hand_temp = ''
        if len(self.top_row.temp_hand) > 0:
            list_top_hand_temp = [str(hand) + ' | ' for hand in self.top_row.temp_hand]
            top_hand_temp = top_hand_temp.join(list_top_hand_temp)

        # mid hand
        mid_hand = ''
        if len(self.mid_row.hand) > 0:
            list_mid_hand = [str(hand) + ' | ' for hand in self.mid_row.hand]
            mid_hand = mid_hand.join(list_mid_hand)

        # mid hand_temp
        mid_hand_temp = ''
        if len(self.mid_row.temp_hand) > 0:
            list_mid_hand = [str(hand) + ' | ' for hand in self.mid_row.temp_hand]
            mid_hand_temp = mid_hand_temp.join(list_mid_hand)

        # bottom hand
        bottom_hand = ''
        if len(self.bottom_row.hand) > 0:
            list_bottom_hand = [str(hand) + ' | ' for hand in self.bottom_row.hand]
            bottom_hand = bottom_hand.join(list_bottom_hand)

        # bottom hand_temp
        bottom_hand_temp = ''
        if len(self.bottom_row.temp_hand) > 0:
            list_mid_hand = [str(hand) + ' | ' for hand in self.bottom_row.temp_hand]
            bottom_hand_temp = bottom_hand_temp.join(list_mid_hand)

        line = '_' * 25

        print(colored(line, 'blue', ))
        print(colored(top_hand, 'white'), end='')
        print(colored(top_hand_temp, 'red', 'on_cyan'))
        print(colored(mid_hand), end='')
        print(colored(mid_hand_temp, 'red', 'on_cyan'))
        print(colored(bottom_hand), end='')
        print(colored(bottom_hand_temp, 'red', 'on_cyan'))
        print(colored(line, 'blue'))


class CardsToPlace(object):
    def __init__(self, cards):
        self.list_of_cards = cards
        self.ready_to_use = [True for _ in range(len(cards))]

    def __str__(self):
        str_hand = ''
        return str_hand.join([str(card) + ' ' for card in self.list_of_cards])

    def print(self):
        colors = {True: ''}
        for card, color in zip(self.list_of_cards, self.ready_to_use):
            if not color:
                print(colored(card, on_color='on_red'), end=' ')
            else:
                print(card, end=' ')

    def get_card(self, card_index: int):
        # card 1 is card 0
        if card_index <= len(self.list_of_cards) + 1:
            self.ready_to_use[card_index - 1] = False
        return self.list_of_cards[card_index - 1]

    def check_if_available(self, card_index):
        if self.ready_to_use[card_index - 1]:
            return True
        else:
            return False

    def reset_card(self):
        self.ready_to_use = [True for _ in self.ready_to_use]


def game(board=None, deck=None):
    # How to play
    # choose a card and to what row it should be placed
    # 2-3  take 2nd card and place it to bottom row
    # key wards:
    # set - if rules allow finish the round and deal cards for next round
    # reset - return cards from board to hand and man can place cards again
    holdings = None
    if board is None:
        print('Next round')
        deck = Deck()
        board = OfcHand()
        holdings = CardsToPlace([deck.get_card() for _ in range(5)])
    elif board.total_cards == 13:
        print(f'Final result is {board.evaluate()}')
        return 0
    else:
        holdings = CardsToPlace([deck.get_card() for _ in range(3)])
    holdings.print()

    for line in fileinput.input():
        line = line.replace('\n', '')
        if line == 'set':
            if (len(holdings.list_of_cards) == 5 and sum(holdings.ready_to_use) == 0) or (
                    len(holdings.list_of_cards) == 3 and sum(holdings.ready_to_use) == 1):
                board.set_changes()
                fileinput.close()
                game(board, deck)
        else:
            print('Number of placed cards is not correct')
        if line == 'reset':
            board.reset()
            holdings.reset_card()
            board.print_hand()
            holdings.print()
            print('hands_reseted')
            continue
        if len(line) > 1:
            card_number = int(line[0])
            to_hand = line[-1]
            if to_hand == '1':
                if holdings.check_if_available(card_number) and not board.top_row.hand_completed:
                    board.add_card(holdings.get_card(card_number), to_hand)
                else:
                    print('Card already used or row is full')
            elif to_hand == '2':
                if holdings.check_if_available(card_number) and not board.mid_row.hand_completed:
                    board.add_card(holdings.get_card(card_number), to_hand)
                else:
                    print('Card already used or row is full ')
            elif to_hand == '3' and not board.bottom_row.hand_completed:
                if holdings.check_if_available(card_number):
                    board.add_card(holdings.get_card(card_number), to_hand)
                else:
                    print('Card already used or row is full ')
            else:
                print(f'Wrong command format write: 1->3 as first card to bottom row')

        board.print_hand()
        holdings.print()


def test_board_look():
    test_hand = OfcHand()
    [test_hand.add_card_to_front(card1) for _ in range(1)]
    [test_hand.add_card_to_front_temp(card1) for _ in range(2)]
    [test_hand.add_card_to_mid(card1) for _ in range(3)]
    [test_hand.add_card_to_mid_temp(card1) for _ in range(2)]
    [test_hand.add_card_to_bottom(card1) for _ in range(3)]
    [test_hand.add_card_to_bottom_temp(card1) for _ in range(2)]
    test_hand.print_hand()


def test_hand_evaluation():
    board = OfcHand(top=[Card(7, 'D'), Card(7, 'C'), Card(8, 'S')],
                    mid=[Card(6, 'S'), Card(5, 'C'), Card(4, 'S'), Card(3, 'C'), Card(2, 'D')],
                    bot=[Card(7, 'S'), Card(5, 'S'), Card(4, 'S'), Card(3, 'S'), Card(2, 'S')])
    board.print_hand()
    board.evaluate()


if __name__ == '__main__':
    # card1 = [Card('1', 'D')]
    # card1 = [Card('1', 'D')]
    # card1 = [Card('1', 'D')]
    card1 = Card('1', 'D')
    card2 = Card('2', 'D')
    straight = [Card('1', 'D'), Card('2', 'D'), Card('3', 'D'), Card('4', 'D'), Card('5', 'S')]
    straight_flush = [Card('1', 'D'), Card('2', 'D'), Card('3', 'D'), Card('4', 'D'), Card('5', 'D')]

    # hs = HandStrength(straight)
    # print(hs.hand_type)
    test_hand = OfcHand()
    #    [test_hand.add_card_to_front(card1) for _ in range(1)]

    # [test_hand.ad(card1) for _ in range(2)]

    # [test_hand.add_card_to_mid(card1) for _ in range(5)]
    # [test_hand.add_card_to_bottom(card2) for _ in range(5)]
    # print(test_hand)
    # init()
    # game()
    test_hand_evaluation()
