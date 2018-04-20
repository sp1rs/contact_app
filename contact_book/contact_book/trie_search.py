import os

import marisa_trie

from contact_book import constants
from contact_book import models

_trie = None


def search_user_by_trie():
    global _trie
    if _trie:
        return _trie

    if os.path.isfile(constants.TRIE_FILE_PATH):
        _trie = marisa_trie.RecordTrie("<L")
        _trie.load(constants.TRIE_FILE_PATH)
        return _trie
    return create_name_and_email_search_trie()


def create_name_and_email_search_trie():
    trie_data = set()
    for name, email, _id in models.Contact.objects.values_list('name', 'email', 'id'):
        trie_data.add((name, (_id, )))
        trie_data.add((name, (_id, )))
    _trie = marisa_trie.RecordTrie('<L', trie_data)
    _trie.save(constants.TRIE_FILE_PATH)
    return _trie
