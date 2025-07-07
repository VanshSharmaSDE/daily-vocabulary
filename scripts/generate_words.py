import datetime
import os
import random
from PyDictionary import PyDictionary

dictionary = PyDictionary()

USED_WORDS_FILE = ".used_words.txt"
COUNTER_FILE = ".word_counter.txt"
README_FILE = "README.md"
ENGLISH_WORD_LIST = "/usr/share/dict/words"

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

def get_random_word(used_words):
    with open(ENGLISH_WORD_LIST, "r") as f:
        words = [w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) > 4]
    tries = 0
    while tries < 50:
        word = random.choice(words)
        if word not in used_words:
            try:
                meanings = dictionary.meaning(word)
                if meanings:
                    for part in ["Noun", "Verb", "Adjective", "Adverb"]:
                        if part in meanings:
                            return word, meanings[part][0]
            except Exception:
                pass
        tries += 1
    return None, None

def main():
    used_words = load_used_words()
    collected = []

    print("🔍 Fetching 5 unique words...")

    while len(collected) < 5:
        word, definition = get_random_word(used_words)
        if word and definition:
            print(f"✅ {word} - {definition}")
            collected.append((word, definition))
            used_words.add(word)

    start_index = get_start_index()
    append_to_readme(collected, start_index)
    update_counter(start_index + len(collected) - 1)
    save_used_words([word for word, _ in collected])
    print("✅ Successfully added to README.md")

if __name__ == "__main__":
    main()
