import random
import datetime
from PyDictionary import PyDictionary
import os

dictionary = PyDictionary()
USED_WORDS_FILE = ".used_words.txt"
README = "README.md"

# A pool of general-use English words
word_bank = [
    "lucid", "aberration", "quintessential", "zenith", "benevolent",
    "candor", "eloquent", "fortitude", "gregarious", "hackneyed",
    "impetuous", "juxtapose", "kinetic", "lament", "meticulous",
    "novel", "obstinate", "placate", "quandary", "resilient",
    "scrupulous", "tenacious", "ubiquitous", "venerable", "wistful",
    "xenophile", "yearn", "zealous"
]

def load_used_words():
    if os.path.exists(USED_WORDS_FILE):
        with open(USED_WORDS_FILE, "r") as f:
            return set(f.read().splitlines())
    return set()

def save_used_words(words):
    with open(USED_WORDS_FILE, "a") as f:
        for word in words:
            f.write(word + "\n")

def append_to_readme(entries):
    today = datetime.datetime.now().strftime("## 📅 %Y-%m-%d")
    with open(README, "a", encoding="utf-8") as f:
        f.write(f"\n\n{today}\n\n")
        for i, (word, definition) in enumerate(entries, 1):
            f.write(f"{i}. **{word.capitalize()}** – {definition}\n")

def main():
    used_words = load_used_words()
    available = list(set(word_bank) - used_words)
    selected_words = random.sample(available, 5)

    collected = []

    for word in selected_words:
        try:
            meaning = dictionary.meaning(word)
            if meaning and "Noun" in meaning:
                definition = meaning["Noun"][0]
            elif meaning and "Verb" in meaning:
                definition = meaning["Verb"][0]
            else:
                continue
            collected.append((word, definition))
        except Exception:
            continue

    if collected:
        append_to_readme(collected)
        save_used_words([w for w, _ in collected])

if __name__ == "__main__":
    main()
