import random
from hangman_Art import HANGMAN_PICS

def hang_words(words):
    try:
        with open(words, 'r') as file:
            words = [line.strip().lower() for line in file if line.strip()]
        easy = [w for w in words if 4 <= len(w) <= 6]
        medium = [w for w in words if 7 <= len(w) <= 9]
        hard = [w for w in words if len(w) >= 10]

        return {
            'easy': easy,
            'medium': medium,
            'hard': hard
        }

    except FileNotFoundError:
        print("Word list file not found!")
        return {'easy': [], 'medium': [], 'hard': []}

def random_word(words_list):
    return random.choice(words_list)

def display_words(word, guessed_letters):
    return ' '.join([letter.upper() if letter in guessed_letters else '_' for letter in word])

def play_hangman(words_list, use_hint=False):
    secret_word = random_word(words_list)
    guessed_letters = []
    wrong_letters = []
    max_attempts = 6
    wrong_count = 0

    if use_hint:
        first_letter = secret_word[0]
        guessed_letters.append(first_letter)
        print(f"\n💡 Hint: The word starts with '{first_letter.upper()}'")

    print("=== Welcome to Hangman game ===")

    while wrong_count < max_attempts:
        print("\nWord:", display_words(secret_word, guessed_letters))
        print("Wrong letters:", ', '.join(wrong_letters))
        print(f"Attempts remaining: {max_attempts - wrong_count}")
        print(HANGMAN_PICS[wrong_count])

        guess = input("Enter a letter: ").lower()

        if not guess.isalpha() or len(guess) != 1:
            print("! Please enter a single valid letter.")
            continue
        if guess in guessed_letters or guess in wrong_letters:
            print("You already guessed that letter.")
            continue
        if guess in secret_word:
            print("Good guess!")
            guessed_letters.append(guess)
        else:
            print("Wrong guess!")
            wrong_letters.append(guess)
            wrong_count += 1

        if all(letter in guessed_letters for letter in secret_word):
            print("\n🎉 Congratulations! You guessed the word:", secret_word.upper())
            return True

    print("\n💀 Game Over! The word was:", secret_word.upper())
    return False

def main():
    wins = 0
    losses = 0

    while True:
        word_buckets = hang_words("words.txt")

        # Custom word addition
        add_word = input("Do you want to add a custom word to the word list? (y/n): ").lower()
        if add_word == 'y':
            new_word = input("Enter the new word (letters only): ").lower()
            if new_word.isalpha():
                with open("words.txt", "a") as file:
                    file.write(f"\n{new_word}")
                print(f"✅ '{new_word}' has been added to the word list.")
            else:
                print("❌ Invalid word. Only letters are allowed.")

        # Mode selection
        mode = input("Choose mode: single or multiplayer? ").lower()
        if mode == "multiplayer":
            secret_word = input("Player 1, enter a word for Player 2 to guess (letters only): ").lower()
            while not secret_word.isalpha():
                secret_word = input("❌ Invalid. Please enter letters only: ").lower()
            print("\n" * 50)  # Clear screen
            result = play_hangman([secret_word], use_hint=False)

        else:  # Single player
            while True:
                difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
                if difficulty in word_buckets and word_buckets[difficulty]:
                    selected_words = word_buckets[difficulty][:]
                    break
                else:
                    print("Invalid choice or no words available for that difficulty.")

            want_hint = input("Do you want a hint for this round? (y/n): ").lower()
            use_hint = (want_hint == 'y')

            result = play_hangman(selected_words, use_hint)

        if result:
            wins += 1
        else:
            losses += 1

        print(f"\n🏁 Score → Wins: {wins} | Losses: {losses}")
        replay = input("Play again (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
