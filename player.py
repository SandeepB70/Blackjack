from card import Card
from hand import Hand
import random

class Player:
    '''
    Represents a regular player in the blackjack game.

    Attributes:
        balance: The player's current balance.
        bet: How much the player bets. Must be a 1 or greater and cannot exceed the player's current balance. 
        splits: The number of splits the player has made. The max number allowed is 3, allowing for a total of four hands.
        double_down: Set to true only if the player has the opportunity to double down and chooses to do so.
    '''
    def __init__(self):
        self.hands = []
        self.balance = 0
        self.bets = []
        self.split = False
        self.splits = 0

    def add_split(self, hand_num, deck):
        '''
        Split the player's hand so they can play on two separate hands. If their hand 
        contains an ace that is being counted as a one, it gets changed to a value of eleven for the new hand.
        '''
        split_card = self.hands[hand_num].cards.pop()
        self.hands[hand_num].total -= split_card.value
        # Adjust an ace being counted as a 1 if it exists
        if split_card.face == 'ace' and split_card.value == 1:
            split_card.value = 11
            self.ace_11 -= 1
        # Add a new hand that will start with the split card
        self.hands.append(Hand())
        self.hands[-1].add_card(split_card)
        # Deal out a new card for each of the new hands
        self.hands[hand_num].add_card(deck.deal())
        self.hands[-1].add_card(deck.deal())
        # Add another bet for the new hand
        self.bets.append(self.bets[0])
        self.splits += 1
        
    def place_bet(self):
        '''
        Obtain a new betting amount from the player. The bet cannot be less than 1 or exceed
        the current balance.
        '''
        while True:
            try:
                new_bet = int(input("Player 1, please enter your betting amount: "))
                if new_bet < 1:
                    print("Please enter a positive number")
                elif new_bet > self.balance:
                    print("Player only has ${} left.".format(self.balance))
                    print("Bet exceeds current balance.")
                else:
                    self.bets.append(new_bet)
                    break
            except ValueError:
                print("Please enter a number.")

''' //OLD_CODE
        def split(self):
        
        Used when a player wants to split their hand. Adjusts the total of their current hand and
        if the card is an ace being counted as a 1 (in the case of a pair of aces), its worth gets readjusted to 11.
        Should not be used by the dealer

        Returns:
            Returns the second card from the player's hand.
        
        card = self.cards.pop()
        self.total -= card.value
        if card.face == 'ace' and card.value == 1:
            card.value = 11
            self.ace_11 -= 1
        return card
'''