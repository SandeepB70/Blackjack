from card import Card, create_deck
from abc import ABCMeta, abstractmethod
import random

class Player:
	'''
	Represents a player of the Blackjack game, who can either be a regular player(Gambler)
	or the dealer. There should only be one dealer for the game.

	Attributes:
		hand_total: How much the player's hand is worth
		hand: The cards that the player holds (starts out empty)
	'''

	__metaclass__= ABCMeta

	def __init__(self):
		self.hand_total = 0
		self.hand = []

	@abstractmethod
	def hit(self, card):
		'''
		Adds a card to the player's hand and increments the hand_total
		'''
		raise NotImplementedError("Subclass forgot to implement 'hit'")

	def contains_ace(self):
		'''
		Only called when a player's hand results in a bust.
		Checks if a player's hand contains an ace being counted as an 11 and changes its value to a 1.

		Returns True if the player's hand contains an ace that was counted as an 11, otherwise returns False.
		'''
		for card in self.hand:
			if card.value == 11:
				card.value = 1
				return True
		else:
			return False

class Dealer(Player):
	'''
	Represents the Dealer.

	Attribute:
		game_deck: The deck that cards will be dealt from. 
	'''
	def __init__(self):
		Player.__init__(self)
		self.game_deck = create_deck()

	def deal(self):
		'''
		Deals out a card from game_deck
		'''
		if len(self.game_deck) == 0:
			raise Exception("Deck is empty")
		else:
			return self.game_deck.pop()

	def hit(self):
		'''
		Deals out a card to the dealer and increases the value of their hand according to the value of 
		the dealt card. Note that an ace is worth 11 by default unless it results in a bust, in which case,
		it is worth 1.
		'''
		self.hand.append(self.deal())

		# Check if this is an ace. It will count as an 11 by default if it 
		# causes the dealer's hand to fall between 17 and 21 (inclusive)
		if self.hand[-1] == 11:
			if (self.hand_total + 11) >= 17 and (self.hand_total + 11) <= 21:
				self.hand_total += 11
			else:
				#Change this ace's value to a 1 so if there is a bust later on, it does not get mistaken for an ace with a value of 11
				self.hand_total[-1].value = 1
				self.hand_total += 1
		# Add the card's value to the hand's total
		else:
			self.hand_total += self.hand[-1].value

class Gambler(Player):
	'''
	Represents a regular player in the blackjack game.

	Attributes:
		balance: The player's current balance.
		bet: How much the player bets. Must be a 1 or greater and cannot exceed the player's current balance. 
	'''
	def __init__(self, balance, bet):
		Player.__init__(self)
		self.balance = balance

		#Make sure the player's bet does not exceed their balance
		if bet > self.balance:
			print("Player only has ${} left.".format(self.balance))
			raise Exception("Bet exceeds current balance.")
		else:
			self.bet = bet

	def place_bet(self):
		'''
		Obtain a new betting amount from the player. The bet cannot be less than 1 or exceed
		the current balance.
		'''

		while True:
			try:
				new_bet = int(input("Player 1, please enter your betting amount: "))
			except ValueError:
				print("Please enter a number.")
				continue
			if new_bet < 1:
				print("Please enter a positive number")
			elif new_bet > self.balance:
				print("Player only has ${} left.".format(self.balance))
				print("Bet exceeds current balance.")
			else:
				self.bet = new_bet
				break

	def add_money(self, amount):
		'''
		Adds money equivalent to the gambler's current bet to their balance.
		'''
		self.balance += amount
		print("New balance: ${}".format(self.balance))

	def withdraw(self):
		'''
		Withdraws money equivalent to the player's current bet from their balance.
		'''
		if self.balance == 0:
			raise Exception("Player has no money.")
		else:
			self.balance -= self.bet
			print("New balance: {}".format(self.balance))

	def hit(self, card):
		self.hand.append(card)
		# Checks if this is an ace. It will count as an 11 by default unless it 
		# causes the player's hand to exceed 21
		if card.value == 11:
			if (self.hand_total + 11) > 21:
				self.hand_total += 1
				# Change this ace's value to a 1 so if there is a bust later on, 
				# it does not get mistaken for an ace with a value of 11
				self.hand[-1].value = 1
			else:
				self.hand_total += 11
		else:
			self.hand_total += card.value