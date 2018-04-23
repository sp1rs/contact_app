from contact_book import constants
from contact_book import elastic_search


def initialize_elasticsearch():
    elastic_search.create_index(constants.ELASTIC_SEARCH_INDEX)
    create_contact_mapping()


def create_contact_mapping():
    mapping = {
        'properties': {
            'contact': {
                'type': 'nested',
                'properties': {
                    'id': {'type': 'long'},
                    'name': {'type': 'text'},
                    'email': {'type': 'text'}
                },
            },
            'created_at': {'type': 'date', 'index': True}
        }
    }
    elastic_search.create_mapping(
        index=constants.ELASTIC_SEARCH_INDEX,
        doc_type=constants.ELASTIC_SEARCH_MAPPING,
        mapping_body=mapping
    )