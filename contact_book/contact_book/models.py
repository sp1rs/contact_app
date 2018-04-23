from django.db import models
from django.utils import timezone

from contact_book import constants


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)


class PhoneNumber(BaseModel):
    PHONE_TYPE = (
        (constants.PhoneNumberType.TYPE_HOME, constants.PhoneNumberType.TYPE_HOME),
        (constants.PhoneNumberType.TYPE_OFFICE, constants.PhoneNumberType.TYPE_OFFICE)
    )

    # Phone number of user.
    number = models.CharField(max_length=16, db_index=True, unique=True)

    # Phone type.
    type = models.CharField(choices=PHONE_TYPE, max_length=10)

    # Phone country code.
    code = models.CharField(max_length=5)

    contact = models.ForeignKey('contact_book.Contact', related_name='numbers')

    @classmethod
    def add(cls, contact_id, number, _type, code):
        """Add phone number to contact.

        Args:
            contact_id (int): Unique contact id.
            number (str): User's phone number.
            code (str): Country code.
            type (str): Phone number type like home or office.

        """
        return PhoneNumber.objects.create(
            contact_id=contact_id,
            type=_type,
            code=code,
            number=number
        )


class Contact(BaseModel):
    name = models.CharField(max_length=31, db_index=True)
    email = models.EmailField(db_index=True, unique=True)
    image_url = models.CharField(max_length=63, null=True)

    @classmethod
    def add(cls, name, email, image_url=None):
        """Add contact.

        Args:
            name (str): User's name.
            email (str): User's email.
            image_url (str): User's image link.

        """
        contact = cls.objects.create(email=email, name=name, image_url=image_url)
        return contact

    @classmethod
    def delete(cls, pk):
        cls.objects.filter(id=pk).delete()

    def to_json(self):
        return {
            'name': self.name,
            'email': self.email,
            'id': self.pk
        }
