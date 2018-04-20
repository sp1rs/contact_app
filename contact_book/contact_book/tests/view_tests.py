import json
import mock

from django.core.urlresolvers import reverse
from django.test import TestCase

from contact_book import exception
from contact_book import models
from contact_book import private
from contact_book.tests import factoryboy


class ViewsTest(TestCase):

    def test_create_contact(self):
        url = reverse('create-contact')
        response = self.client.post(
            url,
            data=json.dumps({
                'email': 'abc@x.com', 'name': 'abc', 'phone_number': '1234567890',
                'code': '+91', 'number_type': 'Home', 'image_url': 'http://xyz.com'
            }),
            content_type='application/json'
        )
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contacts[0].name, 'abc')
        self.assertEqual(contacts[0].email, 'abc@x.com')
        self.assertEqual(contacts[0].numbers.first().number, '1234567890')
        self.assertEqual(contacts[0].numbers.first().code, '+91')
        self.assertEqual(contacts[0].numbers.first().type, 'Home')
        self.assertEqual(response.json(), {'success_message': 'Contact added successfully.'})

        response = self.client.post(
            url,
            data=json.dumps({
                'email': 'abc@x.com', 'name': 'abc', 'phone_number': '1234567890',
                'code': '+91', 'number_type': 'Home', 'image_url': 'http://xyz.com'
            }),
            content_type='application/json'
        )
        self.assertEqual(response.json(), {'error_message': 'Cannot add contact.'})

    def test_update_contact(self):

        # Case 1: Update the contact.
        contact1 = factoryboy.ContactFactory(name='abc')
        url = reverse('update-contact', args=[contact1.id])
        response = self.client.post(
            url, data=json.dumps({'name': 'def'}), content_type='application/json'
        )
        self.assertEqual(response.json(), {'success_message': 'Contact updated successfully.'})
        contacts = models.Contact.objects.all()
        self.assertEqual(contacts.count(), 1)
        self.assertEqual(contacts[0].name, 'def')

        # Case 2: Delete the contact.
        response = self.client.delete(url)
        self.assertEqual(contacts.count(), 0)
        self.assertEqual(response.json(), {'success_message': 'Contact updated successfully.'})

        reverse('update-contact', args=[123123123])
        response = self.client.post(
            url, data=json.dumps({'name': 'def'}), content_type='application/json'
        )
        self.assertEqual(contacts.count(), 0)
        self.assertEqual(response.json(), {'error_message': 'Cannot update contact.'})
