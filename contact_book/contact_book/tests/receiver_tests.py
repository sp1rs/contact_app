import mock

from django.test import TestCase
from django.utils import timezone

from contact_book import constants
from contact_book.tests import factoryboy


class ReceiversTest(TestCase):

    @mock.patch('django.utils.timezone.now')
    @mock.patch('contact_book.receivers.elastic_search.create_document')
    def test_send_contact_to_elasticsearch(self, create_document, now_func):
        now_func.return_value = timezone.datetime(2017, 1, 1, 1, 1)
        contact = factoryboy.ContactFactory()
        create_document.assert_called_with(
            constants.ELASTIC_SEARCH_INDEX,
            constants.ELASTIC_SEARCH_MAPPING,
            {
                'contact': {
                    'id': contact.id,
                    'name': contact.name,
                    'email': contact.email
                },
                'created_at': timezone.datetime(2017, 1, 1, 1, 1)
            }
        )
