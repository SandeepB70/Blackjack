class Hand:
    '''
    Represents a hand that can be held by a player or dealer.

    Attributes:
        cards: The hand of cards the player has. Each card is an object of the Card class.
        total: How much the hand is currently worth.
        ace_11: The number of aces being counted as 11.
    '''

    def __init__(self):
        self.cards = []
        self.total = 0
        self.ace_11 = 0

    def add_card(self, card):
        '''
        Add a card to *cards* and update the *total*. If it is an ace counting as an 11,
        *ace_11* gets incremented.
        '''
        self.cards.append(card)
        #If it's an ace, the total has to be checked to see if it should be worth 1 or 11
        if card.face == 'ace':
            if self.total + 11 > 21:
                card.value = 1
                self.total += 1
            else:
                self.total += card.value
                self.ace_11 += 1
        else:
            self.total += card.value

    def adjust_ace(self):
        '''
        Drops the value of an ace to 1 and decrements *ace_11*. Also drops the *total* by 10 points. 
        Only called when the player's hand results in a bust with an ace.

        Returns:
            True: When an ace worth 11 has been found and adjusted.
            False: When no ace worth 11 has been found.
        '''
        for x in self.cards:
            if x.value == 11:
                x.value = 1
                self.ace_11 -= 1
                self.total -= 10
                return True
        else:
            return False