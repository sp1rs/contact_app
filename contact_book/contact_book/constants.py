from enum import Enum

# Default limit and offset for pagination
DEFAULT_LIMIT = 10
DEFAULT_OFFSET = 0


class PhoneNumberType(Enum):
    TYPE_HOME = 'home'
    TYPE_OFFICE = 'office'

TRIE_FILE_PATH = './trie_search.marisa'