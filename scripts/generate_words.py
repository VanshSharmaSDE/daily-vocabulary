import datetime
import os
from PyDictionary import PyDictionary
from random_word import RandomWords

dictionary = PyDictionary()
random_word = RandomWords()

USED_WORDS_FILE = ".used_words.txt"
COUNTER_FILE = ".word_counter.txt"
README_FILE = "README.md"

def load_used_words():
    if os.path.exists(USED_WORDS_FILE):
        with open(USED_WORDS_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_used_words(words):
    with open(USED_WORDS_FILE, "a") as f:
        for word in words:
            f.write(word + "\n")

def get_start_index():
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip()) + 1
    return 1

def update_counter(new_index):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(new_index))

def append_to_readme(entries, start_index):
    today = datetime.datetime.now().strftime("## 📅 %Y-%m-%d")
    with open(README_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n\n{today}\n\n")
        for i, (word, definition) in enumerate(entries, start=start_index):
            f.write(f"{i}. **{word.capitalize()}** – {definition.strip()}\n\n")

def fetch_unique_word(used_words):
    for _ in range(20):  # Retry limit
        word = random_word.get_random_word()
        if word and word.isalpha() and word.lower() not in used_words:
            meanings = dictionary.meaning(word)
            if meanings:
                for part in ["Noun", "Verb", "Adjective", "Adverb"]:
                    if part in meanings:
                        return word.lower(), meanings[part][0]
    return None, None

def main():
    used_words = load_used_words()
    collected = []

    while len(collected) < 5:
        word, definition = fetch_unique_word(used_words)
        if word and definition:
            collected.append((word, definition))
            used_words.add(word)

    if not collected:
        print("⚠️ No valid words found.")
        return

    start_index = get_start_index()
    append_to_readme(collected, start_index)
    update_counter(start_index + len(collected) - 1)
    save_used_words([word for word, _ in collected])
    print(f"✅ Added {len(collected)} new words to README.md")

if __name__ == "__main__":
    main()
