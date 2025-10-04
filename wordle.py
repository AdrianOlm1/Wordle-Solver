from collections import defaultdict
import math
import numpy as np
import os
from tqdm import tqdm

# Loads all the words that you can guess
global total_words
with open("words.txt", "r") as f:
    total_words = [line.strip() for line in f.readlines()]

# Loads all the words that can be the answer
global answer_words
with open("answer_words.txt", "r") as f:
    answer_words = [line.strip() for line in f.readlines()]

# Dictionary to help with Dynamic Matrix
global word_to_index
word_to_index = {word: i for i, word in enumerate(total_words)}

# Loads Feedback Matrix that stores combinations for all words
def load_feedback_matrix():
    global feedback_matrix
    
    if not os.path.exists("feedback_matrix.npy"):
        print("feedback_matrix.npy not found. Creating a new one...")
        create_feedback_matrix()

    print("Loading Matrix...")
    feedback_matrix = np.load("feedback_matrix.npy")

# Calculates the entropy the total entropy of a word given an array of the possible words
def calculate_entropy(pattern_to_words):
    total_entropy = 0.0
    total_words = sum(len(words) for words in pattern_to_words.values())

    for pattern, words in pattern_to_words.items():
        prob = len(words) / total_words
        entropy = -prob * math.log2(prob)
        total_entropy += entropy

    return total_entropy

# Wordle function to calculate wordle combination
def get_combination(guess, target):
    combination = [''] * 5
    target_chars = list(target)

    # Green pass
    for i in range(5):
        if guess[i] == target[i]:
            combination[i] = 'G'
            target_chars[i] = None

    # Yellow/Black pass
    for i in range(5):
        if combination[i] == '':
            if guess[i] in target_chars:
                combination[i] = 'Y'
                target_chars[target_chars.index(guess[i])] = None
            else:
                combination[i] = 'B'

    return ''.join(combination)

# Creates a feedback matrix to calculate all the possible patterns of each words then stores it at feedback_matrix.npy
def create_feedback_matrix():
    global total_words

    feedback_matrix = np.empty((len(total_words), len(total_words)), dtype = '<U5')

    for i, guess in tqdm(enumerate(total_words), total =len(total_words), desc="Building feedback matrix"):
        for j, answer in enumerate(total_words):
            feedback_matrix[i][j] = get_combination(guess, answer)

    np.save("feedback_matrix.npy", feedback_matrix)

# Calculates the pattern using the feedback_matrix given a guess and a target word
def calculate_combo_feedback(guess, word):
    global feedback_matrix, word_to_index

    guess_index = word_to_index[guess]
    answer_index = word_to_index[word]
    
    pattern = feedback_matrix[guess_index][answer_index]
    return pattern
    

## Function to take in a word and calculate the total distribution of wordle guesses
def calculate_combination_distribution(guessed_word, remainingWords):
    global feedback_matrix, word_to_index

    # Initialize dictionary to store pattern -> words
    pattern_to_words = defaultdict(list)

    # For each word, compute the pattern and store it
    for word in remainingWords:
        pattern = calculate_combo_feedback(guessed_word, word)

        #pattern = get_combination(guessed_word, word)
        pattern_to_words[pattern].append(word)

    return pattern_to_words

## Function to calculate the best guess based on entropy
def calculate_best_guess(remainingWords):
    global total_words
    best_guess = None
    entropy = 0.0

    if len(remainingWords) == 2:
        return remainingWords[0], 1.0

    # Iterate through each words in all words can calculate the best guess
    for word in total_words:
        # Calculate the pattern distribution for the current word
        pattern_to_words = calculate_combination_distribution(word, remainingWords)

        # Calculate the entropy for the current word
        entropy = calculate_entropy(pattern_to_words)

        # check if this is the best guess so far
        if best_guess is None or entropy > best_guess[1]:
            best_guess = (word, entropy)

    return best_guess[0], entropy

def questioning(guess):
    global remainingWords

    # Ask for full 5-letter feedback string
    while True:
        feedback = input(f"Enter Wordle result for '{guess}' (G = green, Y = yellow, B = gray): ").strip().upper()
        if len(feedback) == 5 and all(c in "GYB" for c in feedback):
            break
        print("Invalid input. Please enter exactly 5 characters using only G, Y, and B.")

    # Filter remainingWords to only those that produce the same feedback
    remainingWords = [
        word for word in remainingWords
        if feedback_matrix[word_to_index[guess]][word_to_index[word]] == feedback
        #if get_combination(guess, word) == feedback
    ]

    print(f"{len(remainingWords)} words remaining.")

def wordle_solver():
    global remainingWords
    load_feedback_matrix()
    remainingWords = answer_words.copy()

    for i in range(6):
        if len(remainingWords) == 1:
            print(f"Wordle solved! The word is '{remainingWords[0]}'. Solved in {i+1} guesses.")
            break

        # Calculate the best guess based on entropy
        guess, entropy = ("tares", 3.5023) if i==0 else calculate_best_guess(remainingWords)
        print(f"Best guess: {guess} , Entropy: {entropy:.4f}")

        # Ask for feedback and filter remaining words
        questioning(guess)

if __name__ == "__main__":
    wordle_solver()
    #create_feedback_matrix()