from card import Card
import random

class Deck:
    '''
    Represents the game deck that cards will be drawn from when dealing. 
    Uses the *Card* class to represent the cards.
    '''

    def __init__(self):
        '''
        Creates a list that represents a shuffled standard 52 card deck.

        Return:
            A list that has been shuffled to represent the game deck cards will be taken from.
        '''
        self.deck = []
        for x in Card.suits:
            for key in Card.card_type:
                self.deck.append(Card(key, x))
        random.shuffle(self.deck)
        #TEST CODE to make a split happen for the player and a double down on each split hand.
        split_card1 = Card('six', 'spades')
        split_card2 = Card('six', 'diamonds')
        double_down1 = Card('four', 'hearts')
        self.deck.remove(split_card1)
        self.deck.remove(split_card2)
        self.deck.remove(double_down1)
        self.deck.append(split_card1)
        self.deck.insert(48, split_card2)
        self.deck.insert(47, double_down1)

    def deal(self):
        '''
        Deals the top card from the deck. If the deck is ever empty, a new deck is created
        and dealt from.

        Return:
            A *Card* object that is at the end of the list.
        '''
        try:
            card = self.deck.pop()
            return card
        except IndexError:
            print("Deck is empty. Creating and shuffling new deck...")
            self.__init__()
            return self.deck.pop()
