from django.test import TestCase

from contact_book import models
from contact_book.tests import factoryboy


class ContactModelTest(TestCase):

    def test_add(self):
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 0)

        models.Contact.add('abc', 'abc@x.com')
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contacts[0].email, 'abc@x.com')
        self.assertEqual(contacts[0].name, 'abc')

        models.Contact.add('def', 'abc@y.com')
        self.assertEqual(contacts.count(), 2)
        self.assertEqual(contacts[1].email, 'abc@y.com')
        self.assertEqual(contacts[1].name, 'def')

    def test_delete(self):
        call = factoryboy.ContactFactory()
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 1)

        models.Contact.delete(call.pk)
        self.assertEqual(contacts.count(), 0)
