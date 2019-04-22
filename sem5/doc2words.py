import re

SPLIT_RGX = re.compile(r'\w+', re.U)


def extract_words(text):
    words = re.findall(SPLIT_RGX, text)
    for i in range(len(words)):
        words[i] = words[i].lower()
    return words
