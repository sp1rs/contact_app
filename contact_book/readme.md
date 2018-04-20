## Setup

1. Clone the repo.
`git clone git@github.com:sp1rs/contact_app.git`

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
It hosts 3 apis.
- **`/contact/<contact_id>`** (POST/DELETE)- Update or delete the contact based on method.
- **`/contact/`** (POST)- Create contact.
- **`/contact/all`** (GET)- List the paginated contacts.

## further improvement.
- `Search` api is not yet implemented.
- `Frontend code` is not present.

# Contributors
- Shashank Parekh (sp1rs)
