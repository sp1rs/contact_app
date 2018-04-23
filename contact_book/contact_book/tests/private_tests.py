from django.db import IntegrityError
from django.test import TestCase

from contact_book import exception
from contact_book import models
from contact_book import private
from contact_book.tests import factoryboy


class ContactTest(TestCase):

    def setUp(self):
        super(ContactTest, self).setUp()
        self.contact = private.Contact()

    def test_check_and_create(self):
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 0)

        # Case 1: Test contact.
        self.contact.check_and_create('abc@x.com', 'abc', '1234567890', '+91', 'Home')
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contacts[0].email, 'abc@x.com')
        self.assertEqual(contacts[0].name, 'abc')
        self.assertEqual(contacts[0].numbers.first().number, '1234567890')
        self.assertEqual(contacts[0].numbers.first().code, '+91')
        self.assertEqual(contacts[0].numbers.first().type, 'Home')

        # Case 2: Try to add same contact again.
        with self.assertRaises(exception.ContactException):
            self.contact.check_and_create('abc@x.com', '1234567890', '1', '2', '3')

    def test_check_and_update(self):
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 0)

        # Case 1: Update the contact.
        contact1 = factoryboy.ContactFactory(name='abc', email='abc@x.com')
        self.contact.check_and_update(contact1.id, 'def')
        self.assertEqual(contacts[0].name, 'def')

        # Case 2: Update with wrong contact id.
        with self.assertRaises(exception.ContactException):
            self.contact.check_and_update(123123123, 'xyz')

    def test_delete(self):
        contact1 = factoryboy.ContactFactory()
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 1)

        # Delete the contact.
        self.contact.delete(contact1.pk)

    def test_can_create_contact(self):
        contact1 = factoryboy.ContactFactory()
        contact = private.Contact()
        self.assertFalse(contact._can_create_contact(contact1.email))
        self.assertTrue(contact._can_create_contact('axy@dsdf.com'))

    def test_can_create_update(self):
        contact1 = factoryboy.ContactFactory()
        contact = private.Contact()
        self.assertTrue(contact._can_update_contact(contact1.id))
        self.assertFalse(contact._can_update_contact(123123))

    def test_fetch_list(self):
        contact1 = factoryboy.ContactFactory()
        contact2 = factoryboy.ContactFactory()
        contact3 = factoryboy.ContactFactory()

        phone1 = factoryboy.PhoneNumberFactory(contact=contact1)
        phone2 = factoryboy.PhoneNumberFactory(contact=contact1)
        phone3 = factoryboy.PhoneNumberFactory(contact=contact2)

        contact = private.Contact()
        data = contact.fetch_list(2, 0)
        self.assertDictEqual(
            data[0],
            {
                'id': contact1.id,
                'name': u'xyz',
                'email': contact1.email
            }
        )
        self.assertDictEqual(
            data[1],
            {
                'id': contact2.id,
                'name': u'xyz',
                'email': contact2.email
            }
        )

        data = contact.fetch_list(2, 1)
        self.assertEqual(
            data,
            [
                {
                    'id': contact2.id,
                    'name': u'xyz',
                    'email': contact2.email
                },
                {
                    'id': contact3.id,
                    'name': u'xyz',
                    'email': contact3.email
                }
            ]
        )
