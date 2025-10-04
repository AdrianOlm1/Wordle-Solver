from wordle import calculate_best_guess, calculate_combo_feedback, load_feedback_matrix
import os
import numpy as np
import random

global answer_words
with open("answer_words.txt", "r") as f:
    answer_words = [line.strip() for line in f.readlines()]

global total_words
with open("words.txt", "r") as f:
    total_words = [line.strip() for line in f.readlines()]

global word_to_index
word_to_index = {word: i for i, word in enumerate(total_words)}

###################################################################################################
# The following functions are used for testing the wordle solver
###################################################################################################

## Function to calculate the combination for a given word
def questioning_helper(guess:str, answer:str )-> str:
    feedback = [''] * 5
    answer_chars = list(answer)
    guess_used = [False] * 5

    for i in range(5):
        if guess[i] == answer[i]:
            feedback[i] = 'G'
            answer_chars[i] = None
            guess_used[i] = True
    
    for i in range(5):
        if not feedback[i]:
            if guess[i] in answer_chars:
                feedback[i] = 'Y'
                answer_chars[answer_chars.index(guess[i])] = None
            else:
                feedback[i] = 'B'

    return ''.join(feedback)

## Function to filter remaining words based on combination
def question_tester(guess: str, answer: str):
    global remainingWords, feedback_matrix
    #feedback = questioning_helper(guess, answer)
    pattern = calculate_combo_feedback(guess, answer)

    remainingWords = [
        word for word in remainingWords
        if calculate_combo_feedback(guess, word) == pattern
    ]

## Main loop for each test of wordle
def wordle_tester(answer:str) -> int:
    global remainingWords

    for i in range(6):
        if len(remainingWords) == 1:
            return i + 1
        
        guess, entropy = ("tares",0) if i==0 else calculate_best_guess(remainingWords)

        if guess == answer:
            return i + 1
        
        question_tester(guess,answer)
    return 7

## Function for displaying a histogram of the guesses
def print_histogram(distrbution, fail, total, width=50):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Wordle Solver Progress\n")

    for i in range(1,7):
        count= distrbution[i]
        bar = "█" * int((count /total) * width) if total > 0 else ""
        print(f"{i}: {bar} ({count})")

    fail_bar = "█" * int((fail / total) * width) if total > 0 else ""
    print(f"Fail: {fail_bar} ({fail})")

    avg = sum(i * count for i, count in enumerate(distrbution)) / (total - fail) if total - fail > 0  else 0
    print(f"Average guesses: {avg:.4f}")
    print(f"Fail rate: {fail / total:.2%}")
    print(f"Games played: {total}")

## Function to loop through tester function on a set number of iterations
def tester(iterations:int)->int:
    global remainingWords, feedback_matrix
    distrbution = [0] * 7
    total_guesses = 0
    fail = 0

    feedback_matrix = np.load("feedback_matrix.npy")
    load_feedback_matrix()
    #for i in range(iterations):
    for i in range(len(answer_words)):
        remainingWords = answer_words.copy()

        #random_word = random.choice(remainingWords)
        guessed = wordle_tester(answer_words[i])

        if guessed == 7:
            fail += 1
        else:
            distrbution[guessed] += 1
            total_guesses += guessed

        #if (i + 1) % 2 == 0 or i == iterations - 1:
        print_histogram(distrbution, fail, i + 1)

tester(10000)
