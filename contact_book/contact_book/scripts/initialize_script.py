from contact_book import elastic_search


def initialize_elasticsearch():
    elastic_search.create_index('contact_manager')
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
        index='contact_manager',
        doc_type='contact',
        mapping_body=mapping
    )