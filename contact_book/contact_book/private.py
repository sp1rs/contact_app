from django.db import IntegrityError
from django.db import transaction

from contact_book import constants
from contact_book import exception
from contact_book import models
from contact_book import elastic_search


class Contact(object):

    def __init__(self):
        super(Contact, self).__init__()

    def check_and_create(self, email, name, phone_number, code, number_type, image_url=None):
        """Check and create contact.

        Args:
            email (str): Email address.
            name (str): User's name.
            phone_number (str): User's phone number.
            code (str): Country code.
            number_type (str): Which type of number type.
            image_url (str): Image url for the user.

        Returns:
            (contact_book.models.Contact): Contact object.

        Raises:
            exception.ContactException:

        """
        if not self._can_create_contact(email):
            raise exception.ContactException('Cannot add contact.')
        with transaction.atomic():
            try:
                contact = models.Contact.add(name, email, image_url=image_url)
                models.PhoneNumber.add(contact.pk, phone_number, number_type, code)
            except IntegrityError:
                raise exception.ContactException('Cannot add contact.')
            return contact

    def check_and_update(self, pk, name):
        """Check and update contact data.

        Args:
            pk(int): Unique contact id.
            name(str): User name to be changed.

        Raises:
            exception.ContactException:

        """
        if not self._can_update_contact(pk):
            raise exception.ContactException('Cannot update contact.')
        models.Contact.objects.filter(id=pk).update(name=name)

    def delete(self, pk):
        """Delete the contact.

        Args:
            email(str): Email address.

        """
        models.Contact.delete(pk)

    def fetch_list(self, limit, offset, search_term=''):
        """Return list of paginated contacts. If search term is present then fetch the list from
        the elastic search else search from the db itself.

        Args:
            limit (int): Limit of records.
            offset (int): Limit to be starts with.

        Note:
            Given a search_term, we will search the contact list in elasticsearch for both
            the fields i.e. `email` and `name`.

        """
        final_list = []

        if search_term:
            data = elastic_search.search(
                constants.ELASTIC_SEARCH_INDEX,
                body=self._get_query(search_term),
                **{'from': offset, 'size': limit}
            )
            for contact in data['hits']['hits']:
                final_list.append(contact['_source']['contact'])
        else:
            contacts = models.Contact.objects.all()[offset:(offset + limit)]
            for contact in contacts:
                final_list.append(contact.to_json())
        return final_list

    def _get_query(self, search):
        return {
            'query': {
                'nested':
                    {
                        'path': 'contact',
                        'query': {
                            'multi_match': {
                                'query': search,
                                'type': 'phrase_prefix',
                                'fields': ['contact.name', 'contact.email']
                            }
                        }
                    }
                }
            }


    def _can_create_contact(self, email):
        """Check if contact can be created or not.

        Args:
            email(str): User's email address.

        """
        return not models.Contact.objects.filter(email=email).exists()

    def _can_update_contact(self, pk):
        """Check if contact can be updated or not.

        Args:
            pk(int): User's unique id.

        """
        return models.Contact.objects.filter(id=pk).exists()
