# This program is a chatbot. The algorithm implemented is modelled after the
# ELIZA/DOCTOR script originally developed by Weizenbaum in the 1960s.
#
# CISC 352 Assignment 1
# Sean Nesdoly 10135490
# February 1st, 2017

import re # regular expressions

reflections = {
    "am": "are",
    "was": "were",
    "i": "you",
    "i'd": "you would",
    "i've": "you have",
    "i'll": "you will",
    "my": "your",
    "are": "am",
    "you've": "I have",
    "you'll": "I will",
    "your": "my",
    "yours": "mine",
    "you": "me",
    "me": "you"
}

# take a fragment of text and reflect it back such that each token that matches
# a key in the reflections array is replayed with its corresponding value
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)

def main():
    print "Hello. How are you feeling today?"

    # enter an infinite loop for accepting user input
    while True:
        statement = raw_input("> ")
        print reflect(statement)

        # user input "quit" ends the chatbot
        if statement == "quit":
            break

if __name__ == "__main__":
    main();
