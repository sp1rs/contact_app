from django.apps import AppConfig


class ContactBookConfig(AppConfig):
    name = 'contact_book'
    label = 'contact_book'

    def ready(self):
        from contact_book import receivers
