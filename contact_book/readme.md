## Setup

1. Clone the repo.
`$ git clone git@github.com:sp1rs/contact_app.git`

2. Setup a virtual env with python2
`mkvirtualenv --python=python2.7 contact-app-python2`

3. Activate virtual env
`workon contact-app-python2`

5. Install the requirements.
`pip install -r requirements.txt`

7. To verify things are working fine, run the tests.
`python manage.py test`

# What is contact_app about?
- App which maintain contacts.

## REST APIs
It exposes 3 apis.
- **`/contact/<contact_id>`** (POST/DELETE)- Update or delete the contact based on method.
- **`/contact/`** (POST)- Create contact.
- **`/contact/search?search_term=xyz`** (GET)- List the paginated contacts. And it uses elastic search to fetch the data.


## Elastic search.
- This is used for implementing search based on `name` and `email`.

### Setup Elasticsearch

##### For Mac

- Download and unzip the package from https://www.elastic.co/downloads/elasticsearch
- Go to the downloaded path and run elasticsearch:
```
$ bin/elasticsearch
```

#### To initialize elasticsearch.
- Run this command in the shell.

```
>> from contact_book.scripts import initialize_elastic_search
>> initialize_elastic_search.initialize_elasticsearch()
```


# Contributors
- Shashank Parekh (sp1rs)
