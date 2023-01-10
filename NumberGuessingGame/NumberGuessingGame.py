# Intro
import random


print("Welcome to the Number Guessing Game! ")
print("To play, guess a number between 1 and 10, (including those numbers.) The less guesses you use, the higher your score!")
print()


def Game():
    random_number = random.randint(1,10)
    print()
    attempts = 1

    guess = input("Please enter your first guess: ")
    # adding digit verification so it doesn't break program if letters are used.
    if guess.isdigit():
        guess = int(guess)
    else:
        print("Please type a number: ")

    while guess != random_number:
        attempts += 1
        guess = int(input("Wrong! Guess again: "))

    print("Congratulation! You guessed the number.")

    if attempts == 1:
        print("It took you only " + str(attempts) + " try!")
    else:
        print("It took you " + str(attempts) + " tries.")
    
    
Game()
while input("Would you like to play again? ") == "yes":
    print("Ok! Here we go again.")
    Game()
quit()




    