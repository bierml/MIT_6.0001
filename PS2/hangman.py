# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
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

# end of helper code

# -----------------------------------

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
    flag=True
    for symb in secret_word:
        if symb not in letters_guessed:
            flag=not flag
            break
    return flag


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    if(is_word_guessed(secret_word, letters_guessed)==True):
        return secret_word
    else:
        let_list=[]
        for symb in secret_word:
            if symb in letters_guessed:
                let_list.append(symb)
            else:
                let_list.append('_ ')
        return ''.join(let_list)



def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    lcase_let=list(string.ascii_lowercase)
    for let in letters_guessed:
        if let in lcase_let:
            lcase_let.remove(let)
    return ''.join(lcase_let)
    
    

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
    letters_guessed=[]
    false_letters=[]
    let=''
    guesses_remaining=6
    warnings_remaining=3
    print("Welcome to the game Hangman")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",warnings_remaining,"warnings left")
    while(guesses_remaining>0):
        print("-----------")
        print("You have",guesses_remaining,"guesses left")
        print("Available letters:",get_available_letters(letters_guessed+false_letters))
        let=str.lower(input("Please guess a letter: "))
        if let in letters_guessed:
            if(warnings_remaining>1):
                warnings_remaining-=1
                print("Oops! You've already guessed that letter. You have",warnings_remaining,"warnings left:",get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",get_guessed_word(secret_word, letters_guessed))
                guesses_remaining-=1
        elif let not in string.ascii_lowercase or len(let)!=1:
            if(warnings_remaining>1):
                warnings_remaining-=1
                print("Oops! That is not a valid letter. You have",warnings_remaining,"warnings left:",get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",get_guessed_word(secret_word, letters_guessed))
                guesses_remaining-=1
        elif let not in secret_word:
            false_letters.append(let)
            if(let=='a' or let=='e' or let=='i' or let=='o' or let=='u'):
                guesses_remaining-=2
            else:
                guesses_remaining-=1
            print("Oops! That letter is not in my word:",get_guessed_word(secret_word, letters_guessed))
        else:
            letters_guessed.append(let)
            print("Good guess:",get_guessed_word(secret_word, letters_guessed))
            if(is_word_guessed(secret_word, letters_guessed)==True):
                break
    print("-----------")
    if(guesses_remaining<=0):
        print("Sorry, you ran out of guesses. The word was",secret_word+".")
    else:
        print("Congratulations, you won!")
        print("Your total score for this game is:",guesses_remaining*len(letters_guessed))



# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    parsed_word=''.join(my_word.split())
    if(len(other_word)!=len(parsed_word)):
        return False
    else:
        for i in range(len(other_word)):
            if(parsed_word[i]=='_'):
                if other_word[i] in parsed_word:
                    return False
                continue
            else:
                if(other_word[i]!=parsed_word[i]):
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
    flag=0
    printlist=[]
    for word in wordlist:
        if(match_with_gaps(my_word, word)):
            printlist.append(word)
            flag+=1
            #print(word)
    printlist=' '.join(printlist)
    if(flag==0):
        print("No matches found")
    else:
        print(printlist)
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



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
    letters_guessed=[]
    false_letters=[]
    let=''
    guesses_remaining=6
    warnings_remaining=3
    print("Welcome to the game Hangman")
    print("I am thinking of a word that is",len(secret_word),"letters long.")
    print("You have",warnings_remaining,"warnings left")
    while(guesses_remaining>0):
        print("-----------")
        print("You have",guesses_remaining,"guesses left")
        print("Available letters:",get_available_letters(letters_guessed+false_letters))
        let=str.lower(input("Please guess a letter: "))
        if let=="*":
            print("Possible word matches are:")
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))
            continue
        if let in letters_guessed:
            if(warnings_remaining>1):
                warnings_remaining-=1
                print("Oops! You've already guessed that letter. You have",warnings_remaining,"warnings left:",get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",get_guessed_word(secret_word, letters_guessed))
                guesses_remaining-=1
        elif let not in string.ascii_lowercase or len(let)!=1:
            if(warnings_remaining>1):
                warnings_remaining-=1
                print("Oops! That is not a valid letter. You have",warnings_remaining,"warnings left:",get_guessed_word(secret_word, letters_guessed))
            else:
                print("Oops! You've already guessed that letter. You have no warnings left so you lose one guess:",get_guessed_word(secret_word, letters_guessed))
                guesses_remaining-=1
        elif let not in secret_word:
            false_letters.append(let)
            if(let=='a' or let=='e' or let=='i' or let=='o' or let=='u'):
                guesses_remaining-=2
            else:
                guesses_remaining-=1
            print("Oops! That letter is not in my word:",get_guessed_word(secret_word, letters_guessed))
        else:
            letters_guessed.append(let)
            print("Good guess:",get_guessed_word(secret_word, letters_guessed))
            if(is_word_guessed(secret_word, letters_guessed)==True):
                break
    print("-----------")
    if(guesses_remaining<=0):
        print("Sorry, you ran out of guesses. The word was",secret_word+".")
    else:
        print("Congratulations, you won!")
        print("Your total score for this game is:",guesses_remaining*len(letters_guessed))
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    #secret_word = choose_word(wordlist)
    #hangman(secret_word)
    #print(match_with_gaps("te_ t", "tact"))
    #print(match_with_gaps("a_ _ le", "banana"))
    #print(match_with_gaps("a_ ple", "apple"))
    #print(match_with_gaps("a_ _ le", "apple"))
    #show_possible_matches("a_ pl_ ")
    #show_possible_matches("t_ _ t")
    #show_possible_matches("abbbb_ ")
    #letters_guessed = ['e', 'i', 'k', 'p', 'r', 's']
    #print(get_available_letters(letters_guessed))
    #hangman("word")
###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
