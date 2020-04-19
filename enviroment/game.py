from random import shuffle
import queue
import fileinput
from termcolor import colored

from deprecated import deprecated

top_hand_royalties = {'66': 1, '77': 2, '88': 3, '99': 4, '´1010': 5, '1111': 6, '1212': 7, '1313': 8, '11': 9,
                      '222': 10, '333': 11, '444': 12, '555': 13, '666': 14, '777': 15, '888': 16, '999': 17,
                      '101010': 18, '111111': 19, '121212': 20, '131313': 21, '111': 22}


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

    def __str__(self):
        return f'{self.value}{self.suit}'

    def get_value(self):
        return self.value

    def get_suit(self):
        return self.suit


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        suits = ['S', 'C', 'H', 'D']
        list_of_cards = []
        for rank in range(1, 15):
            for suit in suits:
                list_of_cards.append(Card(rank, suit))

        shuffle(list_of_cards)
        q2 = queue.Queue()
        q2.queue = queue.deque(list_of_cards)
        self.cards = q2

    def get_card(self):
        return self.cards.queue.pop()


class HandStrength(object):

    def __init__(self, cards):

        self.hand_type = 0
        self.hand_name = ''
        self.ranks = [v.get_value() for v in cards]
        self.suit = [v.get_suit() for v in cards]
        self.to_compare = []
        # made hand evaluation
        histogram = {}
        ranks = self.ranks
        ranks.sort()
        if len(ranks) == 5:
            for r in ranks:
                if r in histogram.keys():
                    histogram[r] = histogram[r] + 1
                else:
                    histogram[r] = 1
            hist_values = histogram.values()
            hand_type = {0: 'high', 1: 'pair', 2: 'two_pair', 3: 'trips', 4: 'straight', 5: 'flush', 6: 'full',
                         7: 'quads', 8: 'poker'}
            if max(hist_values) == 4:
                # quads
                self.hand_id = 7
                self.hand_name = hand_type[self.hand_id]
                for rank, quantity in histogram.items():
                    if quantity == 4:
                        self.to_compare = [rank]
            elif len(hist_values) == 2:
                # full
                self.hand_id = 6
                self.hand_name = hand_type[self.hand_id]
                for rank, quantity in histogram.items():
                    if quantity == 2:
                        pair = rank
                    else:
                        trips = rank
                self.to_compare = [trips, pair]
            elif max(hist_values) == 3:
                # trips
                self.hand_id = 3
                self.hand_name = hand_type[self.hand_id]
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
            elif set(self.suit) == 1:
                # self.ranks.sort()
                if ranks[-1] - ranks[0] == 4:
                    self.hand_type = 'straight_flush'
                else:
                    self.hand_type = 'flush'
            elif int(ranks[-1]) - int(ranks[0]) == 4:
                self.hand_type = 'straight'
        else:
            return 0

    def __gt__(self, other):
        if self.hand_id > other.hand_id:
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
        else:
            return False

    def __eq__(self, other):
        # TODO check if hands are equally strong
        pass


class FrontHand(object):
    def __init__(self):
        self.hand = []
        self.ev = 0
        self.royalty = 0
        self.hand_completed = False

    def evaluate(self):
        ranks = [v for v in self.hand]
        if len(ranks) > 1 and len(set(ranks)) < len(ranks):
            if len(ranks) == 3 and len(set(ranks)) == 1:
                hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value(), ranks[2].get_value()])
            else:
                if ranks[0] == ranks[1]:
                    hand_str = ''.join([ranks[0].get_value(), ranks[1].get_value()])
                elif ranks[0] == ranks[2]:
                    hand_str = ''.join([ranks[0].get_value(), ranks[2].get_value()])
                else:
                    hand_str = ''.join([ranks[1].get_value(), ranks[2].get_value()])
                print(f'Hand representation {hand_str}')
            self.ev = top_hand_royalties[hand_str]
        else:
            self.ev = 0.1

    def add_card(self, new_card):
        if isinstance(new_card, list):
            for card in new_card:
                self.hand.append(card)
            if len(self.hand) > 3:
                self.hand_completed = True
                print('To many cards in hand')
        elif isinstance(new_card, Card):
            self.hand.append(new_card)

    # self.evaluate()
    # print(self.ev)

    def hand_strength(self):
        pass


class FrontMidBotHand(object):
    def __init__(self, max_cards=5):
        self.number_of_cards = max_cards
        self.hand = []
        self.temp_hand = []
        self.ev = 0
        self.hand_completed = False

    def evaluate(self):
        if self.number_of_cards == 5:
            hand_type = ''
            # made hand evaluation
            ranks = [v for v in self.hand]
            histogram = {}
            for r in ranks:
                if r in histogram.keys():
                    histogram[r] = histogram[r] + 1
                else:
                    histogram[r] = 1
            hist_values = histogram.values
            if max(hist_values) == 4:
                hand_type = 'quads'
            elif len(hist_values) == 2:
                hand_type = 'Full'
            elif max(hist_values) == 3:
                hand_type = 'trips'
            elif len(hist_values) == 3:
                hand_type = 'twopair'
            elif len(hist_values) == 4:
                hand_type = 'onepair'
        elif self.number_of_cards == 3:
            self.ev = 0

        return self.ev

    def add_card(self, new_card):
        if isinstance(new_card, list):
            for card in new_card:
                self.hand.append(card)
        elif isinstance(new_card, Card):
            self.hand.append(new_card)

            if len(self.hand) == self.number_of_cards:
                self.hand_completed = True

    def add_card_to_temp(self, new_card):
        if isinstance(new_card, list):
            for card in new_card:
                self.hand.append(card)
        elif isinstance(new_card, Card):
            self.hand.append(new_card)

            if len(self.hand) + len(self.temp_hand) == self.number_of_cards:
                self.hand_completed = True

    def set(self):
        self.hand.extend(self.temp_hand)
        self.temp_hand = []

    def reset(self):
        hands_to_return = self.temp_hand
        self.temp_hand = []
        return hands_to_return


class Hand(object):
    def __init__(self):
        self.top_row = FrontMidBotHand(3)
        self.mid_row = FrontMidBotHand(5)
        self.bottom_row = FrontMidBotHand(5)

    def is_it_foul(self):
        front = HandStrength(self.top_row.hand)
        mid = HandStrength(self.mid_row.hand)
        bot = HandStrength(self.mid_row.hand)
        if len(self.top_row.hand) == 3 and len(self.mid_row.hand) == 5 and len(self.mid_row.hand) == 5:
            # OFC rules
            if bot > mid > front:
                return True
            else:
                return False
        else:
            return True

    # if self.bottom_row.hand
    def __str__(self):
        game_look = ''

        # front hand
        top_hand = ''
        list_top_hand = [str(hand) + ' | ' for hand in self.top_row.hand]
        top_hand = top_hand.join(list_top_hand)

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

    def evaluate(self):
        pass

    def add_card_to_front(self, card):
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
            return False

    def add_card_to_bottom(self, card):
        if not self.bottom_row.hand_completed:
            self.bottom_row.add_card(card)
            return True
        else:
            print('Hand is completed')
            return False

    def reset(self):
        pass

    def set_changes(self):
        pass

    def evaluate_hand(self):
        pass


def read_stdin():
    pass


def game():
    random_hand = Deck()
    board_status = Hand()
    starting_hand = [random_hand.get_card() for _ in range(5)]
    burn_hands = []
    [print(x) for x in starting_hand]
    for line in fileinput.input():
        card_number = int(line[0])
        to_hand = line[-2]
        if to_hand == '1':
            board_status.add_card_to_front(starting_hand[card_number])
        elif to_hand == '2':
            board_status.add_card_to_mid(starting_hand[card_number])
        elif to_hand == '3':
            board_status.add_card_to_bottom(starting_hand[card_number])
        else:
            print(f'Wrong command format write: 1->3 as first card to bottom row')

        print(board_status)
    pass


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
    # test_hand = Hand()
    # [test_hand.add_card_to_front(card1) for _ in range(3)]
    # [test_hand.add_card_to_mid(card1) for _ in range(5)]
    # [test_hand.add_card_to_bottom(card2) for _ in range(5)]
    # print(test_hand)
    game()
