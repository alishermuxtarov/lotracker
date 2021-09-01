from hashlib import md5
from textract import process


def integers_only(text) -> str:
    """
    Removes all symbols except integers
    ex: +998(91) 333 33 33 -> 998913333333
    """
    return ''.join(x for x in text if x.isdigit())


def get_boolean(value):
    return value not in ('false', None, 0, 'False', '0')


def get_text_from_file(filename):
    try:
        return process(filename).decode('utf-8')
    except:
        return ''


def md5_text(text):
    return md5(text.encode('utf-8')).hexdigest()