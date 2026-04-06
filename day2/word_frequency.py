"""
Day 2 - Word Frequency Counter

This script reads a text file, cleans the words,
counts how often each word appears, and shows
the top most common words.
"""

from collections import Counter
import string


def count_words(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().lower()

        for ch in string.punctuation:
            text = text.replace(ch, "")

        words = text.split()
        word_counts = Counter(words)

        print("Top 10 most common words:\n")
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")

    except FileNotFoundError:
        print("File not found. Please check the file path.")


if __name__ == "__main__":
    count_words("day2/sample.txt")