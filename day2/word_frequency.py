"""
Day 2 - Advanced Word Frequency Counter

Features:
1. Reads text from a file
2. Converts text to lowercase
3. Removes punctuation
4. Filters common stopwords
5. Counts word frequency
6. Displays top frequent words
7. Shows total words, unique words, and average word length
8. Saves results to an output file
"""

from collections import Counter
import string


STOPWORDS = {
    "the", "is", "and", "in", "to", "of", "a", "an", "it", "for",
    "on", "with", "as", "by", "at", "from", "this", "that", "are",
    "was", "be", "or", "can"
}


def clean_text(text):
    """Convert text to lowercase and remove punctuation."""
    text = text.lower()
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


def extract_words(text):
    """Split text into words and remove stopwords."""
    words = text.split()
    filtered_words = [word for word in words if word not in STOPWORDS]
    return filtered_words


def calculate_average_word_length(words):
    """Calculate average word length."""
    if not words:
        return 0
    total_length = sum(len(word) for word in words)
    return total_length / len(words)


def analyze_text(file_path, output_file="results.txt"):
    """Read file, analyze word frequency, and save results."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        cleaned_text = clean_text(text)
        words = extract_words(cleaned_text)

        if not words:
            print("No valid words found after cleaning the text.")
            return

        word_counts = Counter(words)
        total_words = len(words)
        unique_words = len(word_counts)
        avg_word_length = calculate_average_word_length(words)

        print("\nText Analysis Summary")
        print("-" * 30)
        print(f"Total words       : {total_words}")
        print(f"Unique words      : {unique_words}")
        print(f"Average word length: {avg_word_length:.2f}")

        print("\nTop 10 most common words")
        print("-" * 30)
        for word, count in word_counts.most_common(10):
            print(f"{word}: {count}")

        with open(output_file, "w", encoding="utf-8") as out_file:
            out_file.write("Text Analysis Summary\n")
            out_file.write("-" * 30 + "\n")
            out_file.write(f"Total words: {total_words}\n")
            out_file.write(f"Unique words: {unique_words}\n")
            out_file.write(f"Average word length: {avg_word_length:.2f}\n\n")
            out_file.write("Top 10 most common words\n")
            out_file.write("-" * 30 + "\n")
            for word, count in word_counts.most_common(10):
                out_file.write(f"{word}: {count}\n")

        print(f"\nResults saved to '{output_file}'")

    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    analyze_text("day2/sample.txt")