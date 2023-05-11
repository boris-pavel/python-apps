
# Hangman Game
# -----------------------------------

import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)


# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for c in secret_word:
        if c not in letters_guessed:
            return False
    return True
    


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    s = ''
    for c in secret_word:
        if c not in letters_guessed:
            s += '_ '
        else:
            s += c
    return s.rstrip()



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    s=''
    for c in string.ascii_lowercase:
        if c not in letters_guessed:
            s+=c
    return s

    
def get_unique_letters(word):
    '''
    word: string
    returns: number of unique letters in word
    '''
    unique_letters = []
    for c in word:
        if c not in unique_letters:
            unique_letters.append(c)
    return len(unique_letters)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    vowels = 'aeiou'
    guesses = 6
    warnings = 3
    letters_guessed = []
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have', warnings, 'warnings left.')
    while guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        print('-------------')
        print('You have', guesses, 'guesses left.')
        print('Available letters:', available_letters)
        
        l = str.lower(input('Please guess a letter: '))
        if not str.isalpha(l):
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            else: 
                guesses -= 1
                print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
            continue
        if l in letters_guessed:
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            else: 
                guesses -= 1
                print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
            continue
        
        letters_guessed.append(l)
        if l in secret_word:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        else: 
            if l in vowels:
                guesses -= 2
            else:
                guesses -= 1
            print('Oops! That letter is not in my word.')
            print('Please guess a letter:', get_guessed_word(secret_word, letters_guessed))
        
        if '_' not in get_guessed_word(secret_word, letters_guessed):
            break
        
    print('-------------')
    if guesses > 0:
        print('Congratulations, you won!')
        print('Your total score for this game is:', guesses*get_unique_letters(secret_word))
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word+'.')
        




def format_string(s):
    '''
    s: string with ascii chars, spaces and _
    returns: string without spaces
    '''
    new_s = ''
    for c in s:
        if c in string.ascii_lowercase + '_':
            new_s += c
    return new_s

def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = format_string(my_word)
    
    impossible_letters = ''
    for c in string.ascii_lowercase:
        if c in my_word:
           impossible_letters +=c
    

    if len(my_word) != len(other_word):
        return False
    for i in range(len(my_word)):
        if my_word[i] != other_word[i] and my_word[i] != '_':
            return False
        elif my_word[i] == '_' and other_word[i] in impossible_letters:
            return False
    return True
       


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            possible_matches.append(word)
    if len(possible_matches) == 0:
        print('No matches found')
    else:
        print(' '.join(possible_matches))
           



def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    vowels = 'aeiou'
    guesses = 6
    warnings = 3
    letters_guessed = []
    print('Welcome to the game Hangman!')
    print('I am thinking of a word that is', len(secret_word), 'letters long.')
    print('You have', warnings, 'warnings left.')
    while guesses > 0:
        available_letters = get_available_letters(letters_guessed)
        print('-------------')
        print('You have', guesses, 'guesses left.')
        print('Available letters:', available_letters)
        
        l = str.lower(input('Please guess a letter: '))
        if l == '*':
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        if not str.isalpha(l):
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            else: 
                guesses -= 1
                print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
            continue
        if l in letters_guessed:
            if warnings > 0:
                warnings -= 1
                print('Oops! That is not a valid letter. You have', warnings, 'warnings left:', get_guessed_word(secret_word, letters_guessed))
            else: 
                guesses -= 1
                print('Oops! You\'ve already guessed that letter. You have no warnings left so you lose one guess:', get_guessed_word(secret_word, letters_guessed))
            continue
        
        letters_guessed.append(l)
        if l in secret_word:
            print('Good guess:', get_guessed_word(secret_word, letters_guessed))
        else: 
            if l in vowels:
                guesses -= 2
            else:
                guesses -= 1
            print('Oops! That letter is not in my word.')
            print('Please guess a letter:', get_guessed_word(secret_word, letters_guessed))
        
        if '_' not in get_guessed_word(secret_word, letters_guessed):
            break
        
    print('-------------')
    if guesses > 0:
        print('Congratulations, you won!')
        print('Your total score for this game is:', guesses*get_unique_letters(secret_word))
    else:
        print('Sorry, you ran out of guesses. The word was', secret_word+'.')





if __name__ == "__main__":    
    secret_word = choose_word(wordlist)
    hangman_with_hints('apple')
