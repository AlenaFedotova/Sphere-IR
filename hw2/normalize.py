import re
import string

class TextNormalizer:
    @staticmethod
    def join_numbers(text):
        regex = re.compile('([\d])[\s]+([\d])')
        return regex.sub('\\1\\2', text)

    @staticmethod
    def clean_out_punct(text):
        regex = re.compile('[%s]' % re.escape(string.punctuation + "«" + "»"))
        return regex.sub(' ', text)

    @staticmethod
    def lower_case(text):
        return text.lower()

    @staticmethod
    def remove_entities(text):
        regex = re.compile('&[0-9a-z_A-Z]+;')
        return regex.sub(' ', text)

    
def normalize(text):
    text = TextNormalizer.join_numbers(text)
    text = TextNormalizer.remove_entities(text)
    text = TextNormalizer.clean_out_punct(text)
    text = TextNormalizer.lower_case(text)
    return text
