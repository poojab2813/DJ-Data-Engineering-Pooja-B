import random
from hangman_Art import HANGMAN_PICS

def hang_words(words):
    try:
        with open(words, 'r') as file:
            words = [line.strip().lower() for line in file if line.strip()]
        return words
    except FileNotFoundError:
        print("Word list file not found!")
        return []
    
def random_word(words_list):
    return random.choice(words_list)


def display_words(word, guessed_letters):
    return ' '.join([letter.upper() if letter in guessed_letters else '_' for letter in word])


def play_hangman(words_list):
    
    secret_word = random_word(words_list)
    guessed_letters = []
    wrong_letters = []
    max_attempts = 6
    wrong_count = 0
    
    print("=== Welcome to Hangman game ===")
    
    while wrong_count < max_attempts:
        print("\nWord:", display_words(secret_word,guessed_letters))
        print("Wrong letters:", ', '.join(wrong_letters))
        print(f"Attempts remaining: {max_attempts - wrong_count}")
        print(HANGMAN_PICS[wrong_count])

        
        guess = input("Enter a letter: ").lower()
        
        if not guess.isalpha() or len(guess) != 1:
            print("! Please enter a single valid letter. ")
            continue
        if guess in guessed_letters or guess in wrong_letters:
            print(" you already guessed that letter.")
            continue
        if guess in secret_word:
            print("Good guess!")
            guessed_letters.append(guess)
        else:
            print("Wrong guess!")
            wrong_letters.append(guess)
            wrong_count += 1
        
        if all(letter in guessed_letters for letter in secret_word):
            print("\n Congratulations! you guessed the word: ", secret_word.upper())
            return True
        
    else:
        print("\n Game Over! The word was:", secret_word.upper())
        return False
        
def main():
    word_list = hang_words("words.txt")
    if not word_list:
        return
    
    wins = 0
    losses = 0
    
    while True:
        result = play_hangman(word_list)
        if result:
            wins += 1
        else:
            losses += 1
        
        print(f"\n Score -> wins: {wins} | losses: {losses}")
        replay = input("Play again (y/n):  ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break
        

if __name__=="__main__":
    main()