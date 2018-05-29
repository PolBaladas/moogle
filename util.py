import unicodedata


def clean_word(word):
    """Returns the longest prefix of a word made of latin unicode characters."""
    for i, c in enumerate(word):
        try:
            if not unicodedata.name(c).startswith("latin"):
                return word[:i].lower()
        except:
            pass
    return word.lower()


def clean_words(words):
    """Cleans all words in a string."""
    return " ".join(map(clean_word, words.split()))
