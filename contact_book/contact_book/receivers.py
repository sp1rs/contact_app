from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from contact_book import constants
from contact_book import models
from contact_book import elastic_search


@receiver(post_save, sender=models.Contact)
def send_contact_to_elasticsearch(sender, **kwargs):
    if not kwargs['created']:
        return
    contact = kwargs['instance']
    data = {
        'contact': _get_contact_data(contact),
        'created_at': timezone.now()
    }
    elastic_search.create_document(
        constants.ELASTIC_SEARCH_INDEX,
        constants.ELASTIC_SEARCH_MAPPING,
        data
    )


def _get_contact_data(contact):
    return {
        'id': contact.pk,
        'name': contact.name,
        'email': contact.email
    }
