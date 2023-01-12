# This is a game where the user and computer play Rock, Paper, Scissors against each other.

import random
import time

# LEGEND: 'rock' = 1, 'paper' = 2, 'scissors' = 3



def computer_throw():
    random_number = random.randint(1,3)
    if random_number == 1:
        random_hand = "Rock"
    elif random_number == 2:
        random_hand = "Paper"
    elif random_number == 3:
        random_hand = "Scissors"
    return random_hand, random_number

def user_input():
    user_input = input("Enter your choice: ")

    while user_input != "rock" and user_input != "paper" and user_input != "scissors":
        print("Please enter either 'Rock', 'Paper', or 'Scissors'")
        user_input = input("Enter your choice: ")
        
        
    if user_input.lower() == "rock":
        user_input_digit = 1
            
    elif user_input.lower() == "paper":
        user_input_digit = 2
            
    elif user_input.lower() == "scissors":
        user_input_digit = 3
            
        
    return user_input_digit, user_input

def offense():
    
    computerHand, randomNumber = computer_throw()
    userInputDigit, userHand = user_input()

    if userInputDigit == (randomNumber + 1):
        print("You're still it! " + userHand + " beats " + computerHand + ".")
        return 3 #stay in offense
                
    elif userInputDigit == (randomNumber - 2):
        print("You're still it! " + userHand + " beats " + computerHand + ".")
        return 3 #stay in offense
               
    elif userInputDigit == randomNumber:
        print("You caught him! You both picked " + computerHand + ".")
        return 1 #Won the round
    else:
        print("Now YOU are on the run! " + computerHand + " beats " + userHand + ".")
        return 4 #Switch to defense

def defense():
    
    computerHand, randomNumber = computer_throw()
    userInputDigit, userHand = user_input()

    if userInputDigit == (randomNumber + 1):
        print("Now YOU'RE it! " + userHand + " beats " + computerHand + ".")
        return 3 #switch to offense
                
    elif userInputDigit == (randomNumber - 2):
        print("Now YOU'RE it! " + userHand + " beats " + computerHand + ".")
        return 3 #switch to offense
               
    elif userInputDigit == randomNumber:
        print("He caught you! You both picked " + computerHand + ".")
        return 2 #Lost the round
    else:
        print("You're still on the run! " + computerHand + " beats " + userHand + ".")
        return 4 #stay in defense
        

def muk_jji_bba():
    initialPossession = initial_possession()
    if initialPossession == 1:
            position = offense()
    elif initialPossession == 0:
            position = defense()
    
    
    while position == 3 or position == 4:
        if position == 3:
            position = offense()
        elif position == 4:
            position = defense()

    if position == 1:
        print("You've won the round!")
        return 1
    elif position == 2:
        print("You've lost the round.")
        return 0
       
        

def initial_possession():
    computer_hand, random_number = computer_throw()
    user_input_digit, user_hand = user_input()

    while user_input_digit == random_number:
        print("You tied! You both picked " + computer_hand + ". Please try again: ")
        computer_hand, random_number = computer_throw()
        user_input_digit, user_hand = user_input()

    if user_input_digit == (random_number + 1):
        print("You're it! " + user_hand + " beats " + computer_hand + ".")
        return 1
    elif user_input_digit == (random_number - 2):
        print("You're it! " + user_hand + " beats " + computer_hand + ".")
        return 1
    else:
        print("You are on the run! " + computer_hand + " beats " + user_hand + ".")
        return 0

def display_score(Wins, Rounds):
    my_score = str(Wins)
    comp_score = str(Rounds-Wins)
    
    print("The score is [" + my_score + "," + comp_score + "].")

def run():
    wins = 0
    rounds = 0
    keep_playing = ""
    print("Welcome to MUK JJI PPA, a korean version of Rock, Paper, Scissors.")
    print("Ready to play? ")

    while keep_playing != "no":
        
        wins += muk_jji_bba()

        rounds += 1

        display_score(wins, rounds)

        print()
        play_again = input("Would you like to play again? ")
        if play_again.lower() == "no":
            keep_playing = "no"
            print("Thanks for playing. ")
            


run()