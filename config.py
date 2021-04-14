from card import Card
from hand import Hand
from deck import Deck
from player import Player
from roundResult import RoundResult

'''
Holds the functions responsible for the logic of the Blackjack game. 
    config() sets up a new game.
    new_round() sets up a new round to be played with the same dealer and player
    run_round() contains the logic for carrying out a single round of play

    continue_play() and check_move() are helper functions.
'''

def config(player, dealer, game_deck):
    '''
    Sets up the game by obtaining the player's balance and their betting amount for the first round. 
    The first two cards for the dealer and player are dealt from the deck.
    '''

    # Obtain a balance from the player.
    while True:
        try:
            balance = int(input("Player 1, please enter your total balance: "))
            if balance < 0:
                print("Balance must be a positive number!")
                continue
            else:
                break
        except ValueError:
            print("Please enter a number")
            continue
    player.balance = balance

    # Obtain the betting amount for the player.
    player.place_bet()

    # Begin dealing cards, starting with the player.
    player.hands.append(Hand())
    player.hands[0].add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())
    player.hands[0].add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())

    print("\nPlayer 1's hand contains:", *player.hands[0].cards, sep='\n')
    print("\nDealer's face up card is:\n{}".format(dealer.cards[0]))
    print("") # print a new line

def new_round(player, dealer, game_deck):
    '''
    Starts a new round by clearing out the *dealer* and *player*'s former hands and hand totals. 
    The dealer is given a new deck and two cards are dealt from this deck to the dealer and player.
    '''
    # Reset the dealer and player. The player's balance will not be reset.
    player.hands.clear()
    player.bets.clear()
    player.split = False
    player.splits = 0
    player.hands.append(Hand())
    # Obtain a new betting amount from the player
    player.place_bet()

    dealer.cards.clear()
    dealer.total = 0
    dealer.ace_11 = 0

    # Begin dealing cards, starting with the player.
    player.hands[0].add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())
    player.hands[0].add_card(game_deck.deal())
    dealer.add_card(game_deck.deal())

    print("\nPlayer 1's hand contains:", *player.hands[0].cards, sep='\n')
    print("\nDealer's face up card is:\n{}".format(dealer.cards[0]))
    print("") # print a new line

def run_round(player, dealer, game_deck):
    '''
    Carries out a play of the blackjack game. *player*'s hand is checked for blackjack, followed by the dealer's.
    If no one has blackjack, *player* can choose to hit or stand, while the dealer simply hits until they get 
    at least 17 or bust.

    Return:
        RoundResult enum depending on the outcome of the play.
    '''

    # Check if the player has blackjack
    if player.hands[0].total == 21:
        print("\nPlayer 1 has blackjack")
        # Check if the dealer also has a blackjack, in which case this round is a tie
        if dealer.total == 21:
            print("Dealer's face down card is: {}".format(dealer.cards[1]))
            print("Dealer also has blackjack so this round is a tie.")
            return continue_play()
        # The player has won the round and money will be added to their balance.
        else:
            print("Player 1 wins this round!")
            player.balance += (player.bets[0] * 3/2)
            print("New balance: {0:.2f}".format(player.balance))
            return continue_play()

    # Check if the dealer has a blackjack
    if dealer.total == 21:
        print("\nDealer's face down card is: {}".format(dealer.cards[1]))
        print("Dealer has blackjack and wins this round.")
        player.balance -= player.bets[0]
        print("New balance: {0:.2f}".format(player.balance))
        if player.balance == 0:
            return RoundResult.ZERO_BALANCE
        else:
            return continue_play()

    double1 = False #Indicates if the player doubles down on their first hand
    double2 = False #Indicates if the player doubles down on their second hand
    # Check if the player can split the pair.
    if player.hands[0].cards[0].face == player.hands[0].cards[1].face and (player.bets[0] * 2 <= player.balance):
        while not player.split:
            try:
                move = input("Would you like to split your hand? Enter 'y' for yes or 'n' for no: ").lower()
                if move == 'y':
                    player.split = True
                    player.add_split(0, game_deck)
                    # Play on the first hand
                    print("Playing on first hand:", *player.hands[0].cards, sep = '\n')
                    # Check if the player can double down
                    if player.hands[0].total in [9, 10, 11] and (player.bets[0] * 3) <= player.balance:
                        double1 = double_down(player, 0, game_deck)
                    # Check if the player would like to hit or stand if they didn't double down.
                    if not double1:
                        while True:
                            if hit_stand(player.hands[0], game_deck): # Player has chosen to hit
                                # If the hand total has broken 21, check if it can be adjusted
                                if player.hands[0].total > 21:
                                    if not player.hands[0].adjust_ace():
                                        print("First hand busted")
                                        player.splits -= 1 # This hand basically gets thrown out
                                        player.balance -= player.bets[0]
                                        break
                                elif player.hands[0].total == 21:
                                    break
                            else: # Player has chosen to stand
                                break

                    # Play on the second hand
                    print("Playing on second hand:", *player.hands[1].cards, sep = '\n')
                    if player.hands[1].total in [9, 10, 11]:
                        # If the player already doubled on their first hand, then it needs to be checked
                        # if they could handle up to four times the original bet
                        if double1:
                            if (player.bets[0] * 2) <= player.balance:
                                double2 = double_down(player, 1, game_deck)
                        else:
                            double2 = double_down(player, 1, game_deck)
                    if not double2:
                        while True:
                            if hit_stand(player.hands[1], game_deck):
                                # If the hand total has broken 21, check if it can be adjusted
                                if player.hands[1].total > 21:
                                    if not player.hands[1].adjust_ace():
                                        print("Second hand busted")
                                        player.balance -= player.bets[1]
                                        # If splits are back to 0, then it means the first hand was also a bust.
                                        if player.splits == 0:
                                            return continue_play()
                                        # Otherwise the first hand is still valid.
                                        else:
                                            player.splits -= 1
                                            break
                                elif player.hands[1].total == 21:
                                    break
                            else: #Player has chosen to stand
                                break
                    else: # Player doubled with second hand so break out of loop
                        break
                elif move == 'n':
                    break
                else:
                    print("Enter 'y' or 'n' please.")
            except ValueError:
                print("Please enter 'y' or 'n'.")

    # Check if the player only has one hand. This means they never split and will go through a regular round
    # with one hand. 
    if len(player.hands) == 1:
        option = False # Indicates whether or not a player has chosen to double down
        if player.hands[0].total in [9, 10, 11] and (player.bets[0] * 2) <= player.balance:
            option = double_down(player, 0, game_deck)
        # Start the loop that allows the player to hit or stand if they have not doubled down.
        while not option:
            # Check if they chose to hit
            if hit_stand(player.hands[0], game_deck):
                #Check if the player has busted
                if player.hands[0].total > 21:
                    #Check if they have an ace that has a value of 11
                    if player.hands[0].ace_11 > 0:
                        if player.hands[0].adjust_ace():
                            continue
                        else:
                            print("Error with ace adjustment\n Program will terminate");
                            return RoundResult.ERROR
                    #Player has no ace to adjust so the hand is a bust.
                    else:
                        player.balance -= player.bets[0]
                        print("Player's hand is a bust.")
                        print("New balance: {}".format(player.balance))
                        return continue_play()
                elif player.hands[0].total == 21:
                    print("Player 1 has 21")
                    break
            else:
                break
    
    # Start the loop where the dealer begin to draw cards until they reach at least 17 or bust
    print("\nDealer's face down card is: {}".format(dealer.cards[-1]))
    while True:
        if dealer.total >= 17:
            #If the dealer has a bust, check if their hand has an ace being counted as 11
            if dealer.total > 21:
                adjusted_ace = False #Used to indicate if the dealer has an ace that has been adjusted or not
                if dealer.ace_11 > 0:
                    adjusted_ace = dealer.adjust_ace()
                if not adjusted_ace:
                    print("Dealer's total is {}".format(dealer.total))
                    print("Dealer has busted. Player wins this round.")
                    # If the player split their hand, they should be awarded for each hand
                    if player.splits > 0:
                        if double1:
                            player.balance += player.bets[0]
                        elif player.hand[0].total > 21:
                            player.balance += player.bets[0]
                        if double2:
                            player.balance += player.bets[1]
                        elif player.hand[0].total > 21:
                            player.balance += player.bets[0]
                    else:
                        player.balance += player.bets[0]
                    print("New balance: {0:.2f}".format(player.balance))
                    return continue_play()
            else:
                print("Dealer's hand totals to {}\n".format(dealer.total))
                break
        else:
            dealer.add_card(game_deck.deal())
            print("\nDealer drew: {}".format(dealer.cards[-1]))
            print("Dealer's hand contains:", *dealer.cards, sep='\n')

    check_round(player, dealer)
    if player.balance == 0:
        return RoundResult.ZERO_BALANCE
    return continue_play()

def continue_play():
    '''
    Checks if the Gambler would like to continue playing the game after a round is over.

    Return:
        RoundResult.NEW_ROUND if the Gambler would like to keep playing.
        RoundResult.FINISH if the Gambler wants to stop playing.
    '''

    print("") # Print a new line
    while True:
        try:
            move = input("Would you like to continue playing? Enter 'y' for Yes or 'n' for No: ").lower()
            print("")
            if move == 'y':
                return RoundResult.NEW_ROUND
            elif move =='n':
                return RoundResult.FINISH
            else:
                print("Invalid input!")
                continue
        except ValueError:
            print("Invalid input!")
            continue

def check_move():
    '''
    OLD CODE
    Check the input on whether a Gambler would like to hit or stand.

    Return:
        'h' for hit or 's' for stand
    '''
    while True:
        try:
            move = input("Enter 'h' to hit or 's' to stand: ").lower()
            if move not in {'h', 's'}:
                print("Invalid input")
                continue
            else:               
                return move
        except ValueError:
            print("Invalid input!")

def double_down(player, hand_num, game_deck):
    '''
    '''
    while True:
        try:
            print("Player can double down.")
            move = input("Would you like to? Enter 'y' for Yes or 'n' for No: ").lower()
            if move == 'y':
                player.hands[hand_num].add_card(game_deck.deal())
                #Double the bet
                player.bets[hand_num] *= 2
                print("Player drew: {}\n".format(player.hands[hand_num].cards[-1]))
                return True
            elif move =='n':
                return False
            else:
                print("Invalid input!")
        except ValueError:
            print("Enter 'y' or 'n' please")

def hit_stand(hand, game_deck):
    '''
    Allow the player to choose whether they want to hit or stand.

    Return:
        True: When the player wants to hit
        False: When the player wants to stand
    '''
    while True:
        try:
            move = input("Enter 'h' to hit or 's' to stand: ").lower()
            if move == 'h':
                hand.add_card(game_deck.deal())
                print("Player was dealt: {}".format(hand.cards[-1]))
                print("Current hand: ", *hand.cards, sep = '\n')
                print("Hand total: {}".format(hand.total))
                return True
            elif move == 's':
                return False
        except ValueError:
            print("Invalid input!")

def check_bust(hand):
    '''
    '''
    adjusted = hand.adjust_ace()
    if adjusted:
        return False
    else:
        return True

def check_round(player, dealer):
    '''
    Checks who wins on each hand of the player (if they split). 
    Also adds or subtracts from the player's balance if they won or lost, respectively.
    '''
    for num, hand in enumerate(player.hands, 1):
        if hand.total > dealer.total:
            print("For hand {}, Player wins".format(num))
            player.balance += player.bets[num-1]
            print("New balance: {0:.2f}".format(player.balance))
        elif hand.total < dealer.total:
            print("For hand {}, Player loses".format(num))
            player.balance -= player.bets[num-1]
            print("New balance: {0:.2f}".format(player.balance))
        elif hand.total == dealer.total:
            print("For hand {}, player and dealer tie.".format(num))
        print("") # Print a newline

'''
def check_hand(player):
    
    Check the total value of the player's hand.
    If they bust, check if they have an ace, which will now be counted as a one. 
    Otherwise, they lose the play and cannot continue if their balance has dropped to zero.

    Return:
        RoundResult.CONTINUE if the player can choose to hit or stand again.
        RoundResult.ZERO_BALANCE if the player has no money left.
        RoundResult.TWENTY_ONE if the the player's hand totals to 21.
        RoundResult.NEW_ROUND if the player has lost the round and wants to continue playing the game
        RoundResult.FINISH if the player has chosen to end the game.
    
    if player.hand_total > 21:
        # Subtract 10 so the ace only counts as a 1 instead of an 11
        if player.contains_ace():
            player.hand_total -= 10
            return RoundResult.CONTINUE
        else:
            print("\nTotal of player 1's hand is: {}".format(player.hand_total))
            print("Player 1's hand is a bust")
            print("You lost: ${}".format(player.bet))
            player.withdraw()
            if player.balance == 0:
                return RoundResult.ZERO_BALANCE
            else:
                return continue_play()
    elif player.hand_total == 21:
        print("Player 1 has 21")
        return RoundResult.TWENTY_ONE
    else:
        return RoundResult.CONTINUE
'''