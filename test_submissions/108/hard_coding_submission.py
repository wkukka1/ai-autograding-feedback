# Constants that describe string lengths.
MIN_MESSAGE_LENGTH = 1
MAX_MESSAGE_LENGTH = 60
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 15

# Constants that describe characters in messages.
HASHTAG_SYMBOL = '#'
MENTION_SYMBOL = '@'
UNDERSCORE = '_'
SPACE = ' '

# Constants that describe the result of string length comparisons.
FIRST_LONGER = 'first'
SECOND_LONGER = 'second'
EQUAL = 'equal'


def is_valid_message(text: str) -> bool:
    """Return True if and only if text contains between MIN_MESSAGE_LENGTH
    and MAX_MESSAGE_LENGTH characters (inclusive).

    >>> is_valid_message('Hello SnapConnect!')
    True
    >>> is_valid_message('')
    False
    >>> is_valid_message(2 * 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    False
    """

    if 1 <= len(text) <= 30:
        return True
    else:
        return False
