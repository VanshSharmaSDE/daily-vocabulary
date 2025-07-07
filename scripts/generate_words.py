import datetime
import os
import random
import nltk
from nltk.corpus import wordnet as wn

# File paths
USED_WORDS_FILE = ".used_words.txt"
COUNTER_FILE = ".word_counter.txt"
README_FILE = "README.md"
WORD_LIST_FILE = "data/words.txt"

# Ensure NLTK data is available
nltk.download("wordnet")
nltk.download("omw-1.4")

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
            content = f.read().strip()
            if content.isdigit():
                return int(content) + 1
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

def get_meaning(word):
    synsets = wn.synsets(word)
    if synsets:
        definition = synsets[0].definition()
        if definition and len(definition.split()) > 3:
            return definition
    return None

def get_random_word(used_words, all_words):
    tries = 0
    while tries < 50:
        word = random.choice(all_words)
        if word not in used_words:
            definition = get_meaning(word)
            if definition:
                return word, definition
        tries += 1
    return None, None

def main():
    # Ensure support files exist
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")
    open(USED_WORDS_FILE, "a").close()

    used_words = load_used_words()

    with open(WORD_LIST_FILE, "r") as f:
        all_words = [w.strip().lower() for w in f if w.strip().isalpha() and len(w.strip()) > 4]

    collected = []

    print("🔍 Fetching 5 unique words...")

    while len(collected) < 5:
        word, definition = get_random_word(used_words, all_words)
        if word and definition:
            print(f"✅ {word} - {definition}")
            collected.append((word, definition))
            used_words.add(word)

    if not collected:
        print("⚠️ No valid words found.")
        return

    start_index = get_start_index()
    append_to_readme(collected, start_index)
    update_counter(start_index + len(collected) - 1)
    save_used_words([word for word, _ in collected])
    print("✅ Successfully added to README.md")

if __name__ == "__main__":
    main()
