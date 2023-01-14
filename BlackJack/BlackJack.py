import random
import time
from tkinter import N
from typing import DefaultDict 


def identify_card(number):

    if number >= 1 and number <= 13:
        suit = 'Spades'
        if number < 11:
            if number == 1:
                card_name = 'Ace'
            else:
                card_name = number
        elif number == 11:
            card_name = 'Jack'
            number = 10
        elif number == 12:
            card_name = 'Queen'
            number = 10
        elif number == 13:
            card_name = 'King'
            number = 10
    elif number >= 14 and number <= 26:
        suit = 'Clubs'
        number = number - 13
        if number < 11:
            if number == 1:
                card_name = 'Ace'
            else:
                card_name = number
        elif number == 11:
            card_name = 'Jack'
            number = 10
        elif number == 12:
            card_name = 'Queen'
            number = 10
        elif number == 13:
            card_name = 'King'
            number = 10
    elif number >= 27 and number <= 39:
        suit = 'Hearts'
        number = number - 26
        if number < 11:
            if number == 1:
                card_name = 'Ace'
            else:
                card_name = number
        elif number == 11:
            card_name = 'Jack'
            number = 10
        elif number == 12:
            card_name = 'Queen'
            number = 10
        elif number == 13:
            card_name = 'King'
            number = 10
    elif number >= 40 and number <= 52:
        suit = 'Diamonds'
        number = number - 39
        if number < 11:
            if number == 1:
                card_name = 'Ace'
            else:
                card_name = number
        elif number == 11:
            card_name = 'Jack'
            number = 10
        elif number == 12:
            card_name = 'Queen'
            number = 10
        elif number == 13:
            card_name = 'King'
            number = 10

    return number, card_name, suit


# Passing 'n' to tell us how many cards we want shown face-up, vs not shown at all. (View bottom of method)
def initial_deal(n):
    hand = list(range(2))

    # loop runs twice per method-call, once for each card dealt.
    for i in range(2):
        time.sleep(2)

        # pick a number from our 'deck'.
        number = deck.pop()
        # length = len(deck)
        
        # assign the drawn number to the unique (1/52) card that it represents.
        number, card_name, suit = identify_card(number)
        
        # add the number-value of each card to the hand (list format)
        hand[i] = number

        # this makes it so only ONE of the dealer's two cards is revealed to the user.
        if i <= n: 
            print(str(card_name) + ' of ' + suit)
        elif i > n:
            print('[2nd card hidden]')

    # return our list of two numbers
    return hand

# pulls another card from deck and returns the value of that card
def hit_me():
    time.sleep(2)
    # pull another card from the same deck
    number = deck.pop()

    # identify the unique card that has been drawn
    number, card_name, suit = identify_card(number)

    # display card for user
    print(str(card_name) + ' of ' + suit)

    time.sleep(1)
    return number

def give_user_options(userHand):
    while sum(userHand) <= 21:
        time.sleep(1)
        print()
        choice = input("Would you like to 'hit me' or 'stay'? Type your answer: ")

        while choice != 'hit me' and choice != 'stay':
            choice = input("Please enter either 'hit me' or 'stay': ")

        if choice == 'hit me':
            # draw next card from deck
            next_card = hit_me()
            userHand.append(next_card)
            print(userHand)
        if sum(userHand) > 21:
            print("Bust! You lost this round.")
            userHand = 'bust'
            return userHand
        if sum(userHand) == 21:
            print("21! Lookin good.")
            return userHand
        elif choice == 'stay':
            print("Your hand: " + str(userHand) + " = " + str(sum(userHand)))
            return userHand

def dealers_turn(computerHand, userHand):
    time.sleep(1)
    print()
    print("Now the dealer flips over his card. ")
    time.sleep(1)
    print("Dealer's initial hand: " + str(computerHand))
    time.sleep(1)
    while sum(computerHand) < sum(userHand):
        time.sleep(2)
        print("The dealer draws... ")
        time.sleep(2)
        next_card = hit_me()
        computerHand.append(next_card) 
        print(computerHand)
    if sum(computerHand) == sum(userHand):
        time.sleep(1)
        print("Both parties drew " + sum(computerHand) + ", the dealer wins.")
    elif sum(computerHand) > 21:
        time.sleep(1) 
        print("The dealer has bust! You win this round. ")
    elif sum(computerHand) > sum(userHand):
        time.sleep(1)
        print("The dealer has beat your hand! You've lost this round. ")

print("Welcome back to the Black Jack table.")
print()
time.sleep(1)
print("Here are your two cards: ")


#create new deck and shuffle it
deck  = list(range(52))
random.shuffle(deck)
user_hand = []
computer_hand = []

# view the method directly for explanation of the argument we are passing.
user_hand = initial_deal(1)
time.sleep(1)
print(user_hand) 
print()

time.sleep(2)
print("...and now the dealer's two cards: ")
time.sleep(1)

computer_hand = initial_deal(0)
#print(computer_hand)
print()

user_hand = give_user_options(user_hand)
if user_hand != 'bust':
    dealers_turn(computer_hand, user_hand)
print()


