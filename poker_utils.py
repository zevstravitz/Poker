from enum import Enum, IntEnum
import itertools
import numpy as np

# TODO: Prepend _ to all private methods


class Suit(Enum):
    HEARTS = 'hearts'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'
    SPADES = 'spades'


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class HandType(Enum):
    ROYAL_FLUSH = 9
    STRAIGHT_FLUSH = 8
    FOUR_OF_A_KIND = 7
    FULL_HOUSE = 6
    FLUSH = 5
    STRAIGHT = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    PAIR = 1
    HIGH_CARD = 0


class Card:
    """Class for representing a card."""

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __eq__(self, card2):
        """Two cards equal each other if their suit and rank are the same."""
        return self.suit == card2.suit and self.rank == card2.rank

    def __str__(self):
        # TODO: implement
        return ""

    def __hash__(self):
        if self.suit == Suit.HEARTS:
            result = 0
        elif self.suit == Suit.CLUBS:
            result = 20
        elif self.suit == Suit.SPADES:
            result = 40
        else:
            result = 60
        result += self.rank
        return result

    def __lt__(self, card2):
        return self.rank < card2.rank


class Hand:
    """Represents a standard 5-card poker hand."""

    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('Hand does not contain 5 cards.')
        self.cards = set(cards)
        self.type = self._identify()

    def __str__(self):
        # TODO: Add example string output
        result = ''
        for card in self.cards:
            result += str(card) + '\n'
        return result

    def __gt__(self, hand2):
        """Returns True if the hand is a better hand than hand2."""
        # TODO: Implement
        if self.type.type == hand2.type.type:
            if self.type.rank == hand2.type.rank:
                pass
                # The greatest card in both hands is the same. See if the 2nd
                # biggest cards are the same.

    def chance_of_winning(self, num_opponents):
        """Returns the chance of the hand beating the specified number of opponents.

        Input:
            num_opponents - Number of other players
        """
        chance_against_one = 0
        # TODO: Explain this confusing code
        if self.type == HandType.HIGH_CARD:
            chance_against_one = 0.038552 * (self.type.rank - 1.5)
        elif self.type == HandType.PAIR:
            chance_against_one = 0.501177 + 0.422569 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.TWO_PAIR:
            chance_against_one = 0.923746 + 0.047539 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.THREE_OF_A_KIND:
            chance_against_one = 0.971285 + 0.0211285 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.FULL_HOUSE:
            chance_against_one = 0.992414 + 0.00144058 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.FOUR_OF_A_KIND:
            chance_against_one = 0.993854 + 0.00024 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.STRAIGHT:
            chance_against_one = 0.994094 + 0.00392465 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.FLUSH:
            chance_against_one = 0.998019 + 0.0019654 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.STRAIGHT_FLUSH:
            chance_against_one = 0.999984 + 0.0000138517 / 13 * (self.type.rank - 1.5)
        elif self.type == HandType.ROYAL_FLUSH:
            chance_against_one = 0.999986 + 0.00000153908 / 13 * (self.type.rank - 1.5)
        return chance_against_one ** num_opponents

    def highest_rank(self):
        """Return the highest rank found in self.cards."""
        return max(self.cards)

    def has_rank(self, rank):
        """Returns True if the hand contains a card with the given rank.

        Input:
            rank - A member of the Rank enum class
        """
        for card in self.cards:
            if card.rank == rank:
                return True
        return False

    def _is_royal_flush(self):
        return self._is_straight_flush() and self.has_rank(Rank.ACE)

    def _is_straight_flush(self):
        return self._is_straight() and self._is_flush()

    def _is_n_of_a_kind(self, n):
        """Returns true if the hand is a n-of-a-kind.

        Example: For that is a 4-of-a-kind, _is_n_of_a_kind(4) will be True.
        So will _is_n_of_a_kind(3) and _is_n_of_a_kind(2).

        Input:
            n - How many cards need to be the same rank to return True
        """
        for rank in Rank:
            counter = 0
            for card in self.cards:
                if card.rank == rank:
                    counter += 1
            if counter == n:
                return True
        return False

    # TODO: Also return the rank of the type instead of just the type.
    # For example, a two pair of aces is greater than a two pair of fours.

    def _is_four_of_a_kind(self):
        return self._is_n_of_a_kind(4)

    def _is_full_house(self):
        return self._is_pair() and self._is_three_of_a_kind()

    def _is_flush(self):
        for i, card in enumerate(self.cards):
            if i == 0:
                suit = card.suit
            else:
                if card.suit != suit:
                    return False
        return True

    def _is_straight(self):
        sorted_cards = np.sort(list(self.cards))
        first_rank = sorted_cards[0].rank
        for i, card in enumerate(sorted_cards):
            if card.rank != first_rank + i:
                return False
        return True

    def _is_three_of_a_kind(self):
        return self._is_n_of_a_kind(3)

    def _is_two_pair(self):
        # TODO: Isn't a two pair also technically a pair?
        if self._is_four_of_a_kind() or self._is_pair():
            return False
        num_pairs_found = 0
        for rank in Rank:
            counter = 0
            for card in self.cards:
                if card.rank == rank:
                    counter += 1
            if counter == 2:
                num_pairs_found += 1
        return num_pairs_found == 2

    def _is_pair(self):
        return self._is_n_of_a_kind(2)

    def _identify(self):
        if self._is_royal_flush():
            hand, rank = HandType.ROYAL_FLUSH
        elif self._is_straight_flush():
            hand, rank = HandType.STRAIGHT_FLUSH
        elif self._is_four_of_a_kind():
            hand, rank = HandType.FOUR_OF_A_KIND
        elif self._is_full_house():
            hand, rank = HandType.FULL_HOUSE
        elif self._is_flush():
            hand, rank  = HandType.FLUSH
        elif self._is_straight():
            hand, rank = HandType.STRAIGHT
        elif self._is_three_of_a_kind():
            hand, rank = HandType.THREE_OF_A_KIND
        elif self._is_two_pair():
            hand, rank = HandType.TWO_PAIR
        elif self._is_pair():
            hand, rank = HandType.PAIR
        else:
            hand, rank = HandType.HIGH_CARD
        return hand


def get_deck():
    """Returns a standard 52-card deck as a list of Card instances."""
    deck = []
    for suit in Suit:
        for rank in Rank:
            deck.append(Card(Suit[suit], Rank[rank]))
    return deck


def read_card():
    """Inputs a card from the command line."""
    suit_is_valid = False
    while not suit_is_valid:
        suit_input = input('Suit: ')
        if suit_input in Suit:
            suit_is_valid = True
    rank_is_valid = False
    while not rank_is_valid:
        rank_input = input('Rank: ')
        rank_is_valid = rank_input in Rank
    return Card(suit_input, rank_input)


def best_hand(cards):
    """Returns the best 5-card subset of the given cards.

    Input:
        cards - list of at least 5 Card instances

    Returns:
        Hand instance containing the best possible hand contained in cards.
    """
    return max(generate_all_hands(cards))


def generate_all_hands(cards):
    """Given a list of cards, returns every possible 5-card hand combination.

    Input:
        cards - list of at least 5 Card instances

    Returns:
        hands - list of Hand instances
    """
    if cards.length < 5:
        raise ValueError('Too few cards')
    card_arrays = itertools.combinations(cards, 5)
    hands = []
    for card_array in card_arrays:
        new_hand = Hand(card_array)
        hands.append(new_hand)
    return hands