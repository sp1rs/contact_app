from django.conf import settings

from elasticsearch import Elasticsearch


class ElasticsearchInstance(object):

    def __init__(self):
        self.es = Elasticsearch(settings.ES_HOST)

    def get_instance(self):
        # Send a PING to see if the elasticsearch cluster is up.
        pong = self.es.ping()
        if not pong:
            # Raise exception.
            return
        return self.es


def create_index(index_name, **kwargs):
    """
    Args:
        index_name: Name for the index.
        **kwargs: Other keyword arguments.

    """
    es = ElasticsearchInstance().get_instance()
    return es.indices.create(index=index_name, ignore=400, **kwargs)


def create_mapping(index, doc_type, mapping_body, **kwargs):
    """Creates a mapping for a doc_type in an index

    Args:
        index (string): The name of the index
        doc_type (string): The name of the type
        mapping_body (dict): The body of the mapping
        **kwargs: Other keyword arguments

    """
    es = ElasticsearchInstance().get_instance()
    return es.indices.put_mapping(index=index, doc_type=doc_type, body=mapping_body, **kwargs)


def create_document(index, doc_type, body, **kwargs):
    """Creates document in elasticsearch.

    Args:
        index (string): The name of the index
        doc_type (string): The name of the type
        body (dict): The body of the mapping
        **kwargs: Other keyword arguments

    """
    es = ElasticsearchInstance().get_instance()
    return es.index(index=index, doc_type=doc_type, body=body, **kwargs)


def search(index, body, doc_type=None, **kwargs):
    """Searches data in elasticsearch for a given index and type.

    Args:
        index (string): The name of the index
        doc_type (string): The name of the type
        body (dict): The body of the mapping
        **kwargs: Other keyword arguments

    """
    es = ElasticsearchInstance().get_instance()
    return es.search(index=index, doc_type=doc_type, body=body, params=kwargs)
