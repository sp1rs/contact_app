import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import render

from contact_book import constants
from contact_book import exception
from contact_book import private
from contact_book import utils


@utils.basic_auth()
def create_contact(request, **kwargs):
    """Create contact."""
    data = json.loads(request.body)
    contact = private.Contact()
    try:
        contact.check_and_create(
            data.get('email'), data.get('name'), data.get('phone_number'),
            data.get('code'), data.get('number_type'), data.get('image_url')
        )
    except exception.ContactException as ex:
        return JsonResponse({'error_message': ex.message})

    return JsonResponse({'success_message': 'Contact added successfully.'})


@utils.basic_auth()
def update_contact(request, **kwargs):
    """Update contact."""
    contact_id = kwargs['id']
    contact = private.Contact()
    if request.method.lower() == 'post':
        data = json.loads(request.body)
        try:
            contact.check_and_update(pk=contact_id, name=data.get('name'))
        except exception.ContactException as ex:
            return JsonResponse({'error_message': ex.message})
    elif request.method.lower() == 'delete':
        contact.delete(pk=contact_id)
    return JsonResponse({'success_message': 'Contact updated successfully.'})


def search_contact(request, **kwargs):
    """List contact given limit and offset."""
    limit = int(request.GET.get('limit', constants.DEFAULT_LIMIT))
    offset = int(request.GET.get('offset', constants.DEFAULT_OFFSET))
    search_term = request.GET.get('search_term')
    contact = private.Contact()
    data = contact.fetch_list(limit, offset, search_term)
    return JsonResponse({'objects': data})
