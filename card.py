import random

class Card:
	'''
	Used to represent a playing card. 
	
	Class Object Attributes:
		card_type: A dictionary that associates each face value of a card with its hand value in Blackjack. 
		suits: A list that holds the four suits: Diamonds, Hearts, Clubs, or Spades
	Attributes:
		face: The face of the card as a string (ex. ace, king, two)
		suit: One of the four suits as a string. 
		value: The integer value associated with the card according to the rules of Blackjack. 
		Note that there is only one ace value of 11, but if the player's hand ever busts and they have an ace,
		the Card object respresenting the ace will then have a value of 1.
	'''
	card_type = {'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10,'jack':10,'queen':10,'king':10,'ace':11}
	suits = ['spades', 'clubs', 'hearts', 'diamonds']
	def __init__(self, card_face, suit):
		self.value = Card.card_type[card_face]
		self.face = card_face
		self.suit = suit

	def __str__(self):
		return "{} of {}".format(self.face, self.suit)

def create_deck():
	'''
	Creates a list that represents a standard 52 card deck.

	Return:
		A list that has been shuffled to represent the game deck cards will be taken from.
	'''
	deck = []
	for x in Card.suits:
		for key in Card.card_type:
			deck.append(Card(key, x))
	random.shuffle(deck)
	return deck