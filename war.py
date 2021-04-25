from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple
import random
import itertools
import time


class Suit(Enum):
    Spades = 1
    Hearts = 2
    Clubs = 3
    Diamonds = 4


class Rank(Enum):
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14


@dataclass()
class Card:
    suit: Suit
    rank: Rank

    def __gt__(self, other: "Card"):
        return self.rank.value > other.rank.value

    def __eq__(self, other: "Card"):
        return self.rank.value == other.rank.value

    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name}"


class Deck:
    def __init__(self, name: str = None, initialise=False):
        self.name = name
        self.cards: List[Card] = []
        if initialise:
            self.initialise()

    def put(self, *cards: Card):
        for card in cards:
            self.cards.append(card)

    def pop(self) -> Card:
        card = self.cards.pop()
        if self.name is not None:
            print(f"{self.name} --> {card}", end="\t")
        return card

    def pop_all(self):
        while len(self) > 0:
            yield self.pop()

    def shuffle(self):
        random.shuffle(self.cards)

    def initialise(self):
        for suit in Suit:
            for rank in Rank:
                self.put(Card(suit=suit, rank=rank))
        self.shuffle()

    def deal(self, into: List["Deck"]):
        decks_iter = itertools.cycle(into)
        for card in self.pop_all():
            next(decks_iter).put(card)

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, item):
        return self.cards[item]


class Game:
    def __init__(self, deck_a: Deck, deck_b: Deck):
        self.deck_a = deck_a
        self.deck_b = deck_b
        self.stack_a = Deck()
        self.stack_b = Deck()

    def _both_to_stacks(self, stacks: (Deck, Deck)):
        self._fill_empty_decks()
        stacks[0].put(self.deck_a.pop())
        stacks[1].put(self.deck_b.pop())

    def _fill_empty_decks(self):
        if len(self.deck_a) == 0:
            if len(self.stack_a) > 0:
                print("Player A fills empty deck.")
                self.stack_a.shuffle()
                self.deck_a.put(*self.stack_a.pop_all())
            else:
                raise RuntimeError("Player A lost.")

        if len(self.deck_b) == 0:
            if len(self.stack_b) > 0:
                print("Player B fills empty deck.")
                self.stack_b.shuffle()
                self.deck_b.put(*self.stack_b.pop_all())
            else:
                raise RuntimeError("Player B lost.")

    def _play_round(self):
        temp_stacks = Deck(), Deck()
        self._both_to_stacks(temp_stacks)
        while temp_stacks[0][-1] == temp_stacks[1][-1]:
            self._both_to_stacks(temp_stacks)
            self._both_to_stacks(temp_stacks)
        if temp_stacks[0][-1] > temp_stacks[1][-1]:
            print("Player A wins the round.")
            self.stack_a.put(*temp_stacks[0], *temp_stacks[1])
        else:
            print("Player B wins the round.")
            self.stack_b.put(*temp_stacks[0], *temp_stacks[1])
        # print(f"A deck: {len(self.deck_a)}, A stack: {len(self.stack_a)}")
        # print(f"B deck: {len(self.deck_b)}, B stack: {len(self.stack_b)}")

    def play(self):
        rounds = 0
        try:
            while True:
                self._play_round()
                rounds += 1
                # time.sleep(1)
        except RuntimeError as e:
            print(e)
            print(f"The game took {rounds} rounds.")


def main():
    decks = [Deck("A"), Deck("B")]
    Deck(initialise=True).deal(into=decks)
    game = Game(*decks)
    game.play()


if __name__ == '__main__':
    main()
