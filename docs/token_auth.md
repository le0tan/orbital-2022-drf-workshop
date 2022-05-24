There's a critical problem with the current implementation: while we can CRUD the models via REST APIs, we cannot
register new users in this way! Moreover, we're still using `BasicAuthentication` which requires username and password
for every API call. It's better if we can apply token-based authentication for better security (especially for automated
bots). We will use [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/introduction.html), an extension of
Django REST Framework, to address these two problems.

### Installation

Follow [the instructions](https://dj-rest-auth.readthedocs.io/en/latest/installation.html). Doing the "installation"
section is sufficient. There's no need for the optional ones.

Besides following the steps, there's one more step you need to do: in `ordersys/settings.py`, update
your `DEFAULT_AUTHENTICATION_CLASSES` to include `rest_framework.authentication.TokenAuthentication`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}
```

### Usage

* Get token
    * Request: `POST 127.0.0.1:8000/dj-rest-auth/login/`
    * Response: `{"key": "bca51bf8aa94b4d20d962a30328c606d79310977"}`
* Access API using token
    * Set header: `Authorization: Token <YOUR-TOKEN>`

You can also do email verification and password reset using dj-rest-auth, I'll leave that for your own exploration.