from card import Card, create_deck
from player import Dealer, Gambler
from roundResult import RoundResult

'''
Holds the functions responsible for the logic of the Blackjack game. 
	config() sets up a new game.
	new_round() sets up a new round to be played with the same dealer and player
	run_round() contains the logic for carrying out a single round of play

	continue_play() and check_move() are helper functions.
'''

def config():
	'''
	Sets up the game by creating a dealer and player (one of the gamblers). 
	The bet and balance of the player will be needed to create the player.
	The deal will take place according to the rules of blackjack, two cards for the player and dealer.
	
	Return:
		A tuple containing the player and dealer.
	'''

	print("Setting up game...")
	dealer = Dealer()
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

	# Create the player with an intitial bet of 0
	player1 = Gambler(balance, 0)

	# Obtain the actual betting amount for the player.
	player1.place_bet()

	# Begin dealing cards, starting with the player. 
	# The dealer's second card will not be revealed
	player1.hit(dealer.deal())
	dealer.hit()
	player1.hit(dealer.deal())
	dealer.hit()
	return [dealer, player1]

def new_round(dealer, player1):
	'''
	Starts a new round by clearing out the *dealer* and *player1*'s former hands and hand totals. 
	The dealer is given a new deck and two cards are dealt from this deck to the dealer and player.
	'''

	#Reset the totals of the dealer's and player's hand
	player1.hand_total = 0
	dealer.hand_total = 0
	#Empty the player and dealer's hand
	player1.hand.clear()
	dealer.hand.clear()
	#Obtain a new betting amount from the player
	player1.place_bet()

	#Give the dealer a new deck
	dealer.game_deck = create_deck()

	#Begin dealing cards, starting with the player. 
	#The dealer's second card will not be revealed
	player1.hit(dealer.deal())
	dealer.hit()
	player1.hit(dealer.deal())
	dealer.hit()

def run_round(dealer, player1):
	'''
	Carries out a play of the blackjack game. *player1*'s hand is checked for blackjack, followed by the dealer's.
	If no one has blackjack, *player1* can choose to hit or stand, while the dealer simply hits until they get 
	at least 17 or bust.

	Return:
		RoundResult enum depending on the outcome of the play. 
	'''
	print("Player 1's hand contains: {0} and {1}".format(player1.hand[0], player1.hand[1]))
	print("Dealer's face up card is: {}".format(dealer.hand[0]))

	#Check if anyone has blackjack
	if player1.hand_total == 21:
		print("Player 1 has blackjack")
		#Check if the dealer also has a blackjack, in which case this round is a tie
		if dealer.hand_total == 21:
			print("Dealer's face down card is: {}".format(dealer.hand[1]))
			print("Dealer also has blackjack.\nThis round is a tie.")
			return continue_play()
		#The player has won the round and money will be added to their balance.
		else:
			print("Player 1 wins this round!")
			player1.add_money(player1.bet * 3/2)
			return continue_play()

	#If the dealer's face up card is an ace or one of the face cards, we need to check 
	#the second card to see if the dealer has blackjack
	if dealer.hand[1].face == 'ace' or dealer.hand[1].value == 10:
		if dealer.hand_total == 21:
			print("Dealer's face down card is: {}".format(dealer.hand[1]))
			print("Dealer has blackjack.\nDealer wins this round.")
			player1.withdraw()
			if player1.balance == 0:
				return RoundResult.ZERO_BALANCE
			else:
				return continue_play()

	# Start the loop that allows the player to hit or stand.
	while True:
		player_move = check_move()
		if player_move == 's':
			break
		if player_move == 'h':
			player1.hit(dealer.deal())
			print("Player drew: {}".format(player1.hand[-1]))
		# Check the total value of the player's hand.
		# If they bust, check if they have an ace, which will now be counted as a one. 
		# Otherwise, they lose the play and cannot continue if their balance has dropped to zero.
		if player1.hand_total > 21:
			# Subtract 10 so the ace only counts as a 1 instead of an 11
			if player1.contains_ace():
				player1.hand_total -= 10
				continue
			else:
				print("Total of player 1's hand is: {}".format(player1.hand_total))
				print("Player 1's hand is a bust")
				print("You lost: ${}".format(player1.bet))
				player1.withdraw()
				if player1.balance == 0:
					return RoundResult.ZERO_BALANCE
				else:
					return continue_play()
				break
		elif player1.hand_total == 21:
			print("Player 1 has 21")
			break
		# Player has not reached 21 and did not bust so they can choose to hit or stand again
		else:
			continue

	# Start the loop where the dealer begin to draw cards until they reach at least 17 or bust
	print("Dealer's face down card is: {}".format(dealer.hand[1]))
	while True:
		if dealer.hand_total >= 17:
			#If the dealer has a bust, check if their hand has an ace being counted as 11
			if dealer.hand_total > 21 and dealer.contains_ace():
				dealer.hand_total -= 10
				continue
			else:
				("Dealer's hand totals to {}".format(dealer.hand_total))
				break
		else:
			dealer.hit()
			print("Dealer drew: {}".format(dealer.hand[-1]))

	# Check if the dealer busted
	print("Player's hand has a total of {}".format(player1.hand_total))
	print("Dealer's hand has a total of {}".format(dealer.hand_total))

	if dealer.hand_total > 21:
		print("Dealer has a bust. Player 1 wins this round")
		player1.add_money(player1.bet)
		return continue_play()
	elif dealer.hand_total > player1.hand_total:
		print("Dealer wins this round")
		player1.withdraw()
		if player1.balance == 0:
			return RoundResult.ZERO_BALANCE
		else:
			return continue_play()
	elif dealer.hand_total < player1.hand_total:
		print("Player 1 wins this round")
		player1.add_money(player1.bet)
		return continue_play()
	else:
		print("Round is a draw")
		return continue_play()

def continue_play():
	'''
	Checks if the Gambler would like to continue playing the game after a round is over.

	Return:
		RoundResult.NEW_ROUND if the Gambler would like to keep playing.
		RoundResult.FINISH if the Gambler wants to stop playing.
	'''
	while True:
		try:
			move = input("Would you like to continue playing?\nEnter 'y' for Yes or 'n' for No: ").lower()
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