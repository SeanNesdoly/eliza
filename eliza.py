# This program is an implementation of a classic chatbot. The algorithm implemented
# is modelled after the Eliza script originally developed by Weizenbaum in the 1960s.
# The user is initially prompted for an input phrase. A statement that is meant to convey
# understanding to the user is reflected back by means of an algorithmic transformation
# on the input string.
#
# CISC 352 Assignment 1
# Sean Nesdoly 10135490
# February 1st, 2017

import re # regular expressions
import random
import argparse # command line arguments
from collections import deque

# set optional argument for "terminal-mode"
# this flag determines whether user input is read from a file or from stdin
TERM_MODE = False

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--terminal", help="chatbot accepts user input from stdin (instead of a file)", action="store_true")
args = parser.parse_args()
if args.terminal:
    print "terminal-mode turned on"
    TERM_MODE = True

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
    "you": "i", # swap for me instead?
    "me": "you"
}

psychobabble = {
    r'I need (.*)':
        ["Why do you need {0}?",
         "Would it really help you to get {0}?",
         "Are you sure you need {0}?"],

    r'Why don\'?t you ([^\?]*)\??':
        ["Do you really think I don't {0}?",
         "Perhaps eventually I will {0}.",
         "Do you really want me to {0}?"],

    r'Why can\'?t I ([^\?]*)\??':
        ["Do you think you should be able to {0}?",
         "If you could {0}, what would you do?",
         "I don't know -- why can't you {0}?",
         "Have you really tried?"],

    r'I can\'?t (.*)':
        ["How do you know you can't {0}?",
         "Perhaps you could {0} if you tried.",
         "What would it take for you to {0}?"],

    r'I am (.*)':
        ["Did you come to me because you are {0}?",
         "How long have you been {0}?",
         "How do you feel about being {0}?"],

    r'I\'?m (.*)':
        ["How does being {0} make you feel?",
         "Do you enjoy being {0}?",
         "Why do you tell me you're {0}?",
         "Why do you think you're {0}?"],

    r'Are you ([^\?]*)\??':
        ["Why does it matter whether I am {0}?",
         "Would you prefer it if I were not {0}?",
         "Perhaps you believe I am {0}.",
         "I may be {0} -- what do you think?"],

    r'What (.*)':
        ["Why do you ask?",
         "How would an answer to that help you?",
         "What do you think?"],

    r'How (.*)':
        ["How do you suppose?",
         "Perhaps you can answer your own question.",
         "What is it you're really asking?"],

    r'Because (.*)':
        ["Is that the real reason?",
         "What other reasons come to mind?",
         "Does that reason apply to anything else?",
         "If {0}, what else must be true?"],

    r'(.*) sorry (.*)':
        ["There are many times when no apology is needed.",
         "What feelings do you have when you apologize?"],

    r'Hello(.*)':
        ["Hello... I'm glad you could drop by today.",
         "Hi there... how are you today?",
         "Hello, how are you feeling today?"],

    r'I think (.*)':
        ["Do you doubt {0}?",
         "Do you really think so?",
         "But you're not sure {0}?"],

    r'(.*) friend (.*)':
        ["Tell me more about your friends.",
         "When you think of a friend, what comes to mind?",
         "Why don't you tell me about a childhood friend?"],

    r'Yes':
        ["You seem quite sure.",
         "OK, but can you elaborate a bit?"],

    r'(.*) computer(.*)':
        ["Are you really talking about me?",
         "Does it seem strange to talk to a computer?",
          "How do computers make you feel?",
          "Do you feel threatened by computers?"],

    r'Is it (.*)':
        ["Do you think it is {0}?",
         "Perhaps it's {0} -- what do you think?",
         "If it were {0}, what would you do?",
         "It could well be that {0}."],

    r'It is (.*)':
        ["You seem very certain.",
         "If I told you that it probably isn't {0}, what would you feel?"],

    r'Can you ([^\?]*)\??':
        ["What makes you think I can't {0}?",
         "If I could {0}, then what?",
         "Why do you ask if I can {0}?"],

    r'Can I ([^\?]*)\??':
        ["Perhaps you don't want to {0}.",
         "Do you want to be able to {0}?",
         "If you could {0}, would you?"],

    r'You are (.*)':
        ["Why do you think I am {0}?",
         "Does it please you to think that I'm {0}?",
         "Perhaps you would like me to be {0}.",
         "Perhaps you're really talking about yourself?"],

    r'You\'?re (.*)':
        ["Why do you say I am {0}?",
        "Why do you think I am {0}?",
        "Are we talking about you, or me?"],

    r'I don\'?t (.*)':
        ["Don't you really {0}?",
         "Why don't you {0}?",
         "Do you want to {0}?"],

    r'I feel (.*)':
        ["Good, tell me more about these feelings.",
         "Do you often feel {0}?",
         "When do you usually feel {0}?",
         "When you feel {0}, what do you do?"],

    r'I have (.*)':
        ["Why do you tell me that you've {0}?",
         "Have you really {0}?",
         "Now that you have {0}, what will you do next?"],

    r'I would (.*)':
        ["Could you explain why you would {0}?",
         "Why would you {0}?",
         "Who else knows that you would {0}?"],

    r'Is there (.*)':
        ["Do you think there is {0}?",
         "It's likely that there is {0}.",
         "Would you like there to be {0}?"],

    r'My (.*)':
        ["I see, your {0}.",
         "Why do you say that your {0}?",
         "When your {0}, how do you feel?"],

    r'You (.*)':
        ["We should be discussing you, not me.",
         "Why do you say that about me?",
         "Why do you care whether I {0}?"],

    r'Why (.*)':
        ["Why don't you tell me the reason why {0}?",
         "Why do you think {0}?"],

    r'I want (.*)':
        ["What would it mean to you if you got {0}?",
         "Why do you want {0}?",
         "What would you do if you got {0}?",
         "If you got {0}, then what would you do?"],

    r'(.*) mother(.*)':
        ["Tell me more about your mother.",
         "What was your relationship with your mother like?",
         "How do you feel about your mother?",
         "How does this relate to your feelings today?",
         "Good family relations are important."],

    r'(.*) father(.*)':
        ["Tell me more about your father.",
         "How did your father make you feel?",
         "How do you feel about your father?",
         "Does your relationship with your father relate to your feelings today?",
         "Do you have trouble showing affection with your family?"],

    r'(.*) child(.*)':
        ["Did you have close friends as a child?",
         "What is your favorite childhood memory?",
         "Do you remember any dreams or nightmares from childhood?",
         "Did the other children sometimes tease you?",
         "How do you think your childhood experiences relate to your feelings today?"],

    r'(.*)\?':
        ["Why do you ask that?",
         "Please consider whether you can answer your own question.",
         "Perhaps the answer lies within yourself?",
         "Why don't you tell me?"],

    r'quit':
        ["Thank you for talking with me.",
         "Good-bye.",
         "Thank you, that will be $652. Have a good day!"],

    r'(.*)':
        ["Please tell me more.",
         "Let's change focus a bit... Tell me about your family.",
         "Can you elaborate on that?",
         "Why do you say that {0}?",
         "I see.",
         "Very interesting.",
         "{0}.",
         "I see. And what does that tell you?",
         "How does that make you feel?",
         "How do you feel when you say that?"]
}

# TODO: ranking: more matches within a statement ranks high; more specific matches (mother) ranks high; rank key words?

# TODO: memory implementation (stack)

# TODO: add & refine psychobabble responses

# TODO: a matched pattern should randomly select a response; reduce repition of psychobabble

# initialize the global memory queue that stores keywords with rank>0 for later use
memory_queue = deque()

quit_strings = [
    "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $652. Have a good day!"]

generic_responses = [
    "Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Can you elaborate on that?",
    "Why do you say that {0}?",
    "I see.",
    "Very interesting.",
    "{0}.",
    "I see. And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?",
    "Please go on.",
    "Does talking about this bother you?",
    "I'm not sure I understand you fully."]

keywords = {

    "sorry": [0, [r'(.*)',
        ["Please don't apologise.",
        "Apologies are not necessary.",
        "I've told you that apologies are not required.",
        "It did not bother me. Please continue."]], False],

    "apologise": [0, [r'(.*)',
        ["=sorry"]], False],

    "remember": [5,
        [r'(.*)I remember (.*)',
            ["Do you often think of {1}?",
            "Does thinking of {1} bring anything else to mind?",
            "What else do you recollect?",
            "Why do you remember {1} just now?",
            "What in the present situation reminds you of {1}?",
            "What is the connection between me and {1}?",
            "What else does {1} remind you of?"]],

        [r'(.*)do you remember (.*)',
            ["Did you think I would forget {1}?",
            "Why do you think I should recall {1} now?",
            "What about {1}?",
            "=what",
            "You mentioned {1}?"]], True],

    "dreamed": [5, [r'(.*)I dreamed (.*)',
        ["Really, {1}?",
        "Have you ever fantasized {1} while you were awake?",
        "Have you ever dreamed {1} before?"]], False],

    "my": [5, [r'(.*) my (.*)',
        ["Let's discuss further why your {1}.",
        "Earlier you said your {1}.",
        "But your {1}.",
        "Does that have anything to do with the fact that your {1}?"]], True],

}


# take a fragment of text and reflect it back such that each token that matches
# a key in the reflections array is replaced with its corresponding value
def reflect(fragment):
    tokens = fragment.lower().split()
    for i, token in enumerate(tokens):
        if token in reflections:
            tokens[i] = reflections[token]
    return ' '.join(tokens)


# select out keywords from the input string and build up a keystack such that
# the highest ranking keyword is at the top
def build_keystack(statement):
    tokens = statement.lower().split()
    keystack = []
    for i, token in enumerate(tokens):
        key_rank = token[0]
        if token in keywords:
            if not keystack: # no keys yet, so simply add it in
                keystack = [keywords[token]]
            elif key_rank > keystack[-1][0]: # add higher rank key to the top of the stack (end of list)
                keystack.extend([keywords[token]])
            else: # add low ranking key to bottom of stack (beginning of list)
                keystack.insert(0, keywords[token])

    return keystack


def transform(statement):
    keystack = build_keystack(statement)

    # initial iteration over matched_keys to determine how many matches have occurred

    # keep track of the number of additions to memory for the current transformation
    # to prevent stored responses being used immediately
    num_mem_additions = 0

    for matched_key in reversed(keystack):
        # for each matched key, we loop through all regex to find a match!
        for i in range(1, len(matched_key)-1):
            # parse out key contents of current regular expression
            key_regex = matched_key[i][0]
            key_responses = matched_key[i][1]

            match = re.match(key_regex, statement.rstrip(".!"))
            if match:
                # for this regex match, randomly select a response
                response = random.choice(key_responses)

                # selected response refers to another keyword
                if "=" in response:
                    # parse out a random response from the "pointed-to" keyword
                    related_keyword = keywords[response[1:]]
                    new_responses = related_keyword[1][1]
                    response = random.choice(new_responses)

                # reflect response back by swapping first person for second person & vice-versa
                reflected_response = response.format(*[reflect(g) for g in match.groups()])

                # add the key to memory if the MEMORY flag is set
                if matched_key[2] == True:
                    memory_queue.append(reflected_response)
                    num_mem_additions += 1
                    continue # store the response in memory & select a new keyword from the keystack

                return reflected_response

    # if we have made it here, no keyword in the statement contains a matching regex for transformation.
    # We will randomly decide to select a response
    #    -from memory (if one exists), or,
    #    -by generating a content-free response
    if memory_queue and len(memory_queue)>num_mem_additions and random.random()>0.5:
        response = memory_queue.popleft() # select the oldest response out of memory
    else: # generate a content-free remark!
        response = random.choice(generic_responses).format(*[reflect(statement)])

    return response


def analyze(statement):
    for pattern, responses in psychobabble.items():
        match = re.match(pattern, statement.rstrip(".!"))
        if match:
            print pattern
            response = random.choice(responses)
            return response.format(*[reflect(g) for g in match.groups()])


def main():
    print "Hello. How are you feeling today?"

    if TERM_MODE: # enter an infinite loop for accepting user input from stdin
        while True:
            statement = raw_input("> ")

            # user input "quit" terminates the chatbot
            if statement == "quit":
                print random.choice(quit_strings)
                break

            # apply a transformation to the input string
            print transform(statement)

    else: # parse user input from file
        human_script = open('human_script.txt', 'r')

        # read the file one line at a time, applying the transformation algorithm to each one in a sequential order
        for line in human_script:
            print ">", line.strip() # strip new line character

            # a line with the string "quit" terminates the chatbot
            if line == "quit":
                print random.choice(quit_strings)
                break

            # apply a transformation to the input line
            print transform(line)

        human_script.close()

if __name__ == "__main__":
    main();
