import factory

from factory.django import DjangoModelFactory

from contact_book import models


class ContactFactory(DjangoModelFactory):
    FACTORY_FOR = models.Contact

    name = 'xyz'
    email = factory.Sequence(lambda n: 'test%s@example.com' % n)


class PhoneNumberFactory(DjangoModelFactory):
    FACTORY_FOR = models.PhoneNumber

    number = factory.Sequence(lambda n: '123456789%s' % n)
    type = 'Home'
    code = '+91'
    contact = factory.SubFactory(ContactFactory)
