# This is a game where the user and computer play Rock, Paper, Scissors against each other.

import random
import time

# LEGEND: 'rock' = 1, 'paper' = 2, 'scissors' = 3

print("Ready to play, rock, paper scissors? ")




while True:
    random_number = random.randint(1,3)
    if random_number == 1:
        random_hand = "Rock"
    elif random_number == 2:
        random_hand = "Paper"
    elif random_number == 3:
        random_hand = "Scissors"

    while True:
        user_input = input("Enter your choice: ")
        if user_input.lower() == "rock":
            user_input_digit = 1
            break
        elif user_input.lower() == "paper":
            user_input_digit = 2
            break
        elif user_input.lower() == "scissors":
            user_input_digit = 3
            break
        else:
            print("Please enter either 'Rock', 'Paper', or 'Scissors'")
            continue


    if user_input_digit == (random_number + 1):
        print("You win! " + user_input + " beats " + random_hand + ".")
    elif user_input_digit == (random_number - 2):
        print("You win! " + user_input + " beats " + random_hand + ".")
    elif user_input_digit == random_number:
        print("You tied! You both picked " + random_hand + ". Please try again: ")
        continue
    else:
        print("You lose! " + random_hand + " beats " + user_input + ".")

    print()
    play_again = input("Would you like to play again? ")
    if play_again.lower() == "no":
        print("Thanks for playing. ")
        break

    