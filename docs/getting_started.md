## Installation

1. [Django](https://docs.djangoproject.com/en/4.0/topics/install/#installing-official-release)
2. [(Will cover later) Django Rest Framework](https://www.django-rest-framework.org/#installation)
3. [(Will cover later) dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/installation.html)

### Create Django Project

1. `python -m django --version` to check you have Django properly installed in your current environment.
2. `django-admin startproject ordersys`
3. `python manage.py runserver`

### Add Django Application

* Project vs. App
    * Project = configuration (settings.py) + a collection of apps
    * App = a web application that does something
        * An app can appear in multiple projects
        * A project can include multiple apps
        * e.g., Django REST Framework is an app
* Start an app: `python manage.py startapp app`
    * Naming is hard, please come up with a more creative name for your own project =)
* Include app in the project: `INSTALLED_APPS` from `settings.py`
    * Add `app.apps.AppConfig` to the list

## Django URL (i.e., Router) and View

With your Django app properly initialized, you should see the following welcome page:
![](attachments/Pasted%20image%2020220519160407.png)
Now let's briefly talk about how to setup a URL router in Django and display our own web page (or in Django terms, view)
.

### Creating a Simple View

In `app/views.py`:

```python
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello world!")
```

We now created a view named `index` which simply responds with a string of text.

### Creating Routes to Our View

1. Create a new file `app/urls.py`:

```python
from django.urls import path

from . import views

urlpatterns = [
    # `name` arg is optional, but helpful for `reverse()` function
    # ref: https://docs.djangoproject.com/en/4.0/topics/http/urls/#naming-url-patterns
    path('', views.index, name='index'),
]
```

A `urls.py` file will have a list named `urlpatterns`, inside which are `path`s that corresponds to the `view`s in
this *app*. A `path` requires two arguments: `route` and `view`. `route` is basically a URL that Django URL Dispatcher
attempts to match, and `view` is the view Django returns if the URL is a match.

For more details about Django URL Dispatcher, please refer
to [here](https://docs.djangoproject.com/en/4.0/topics/http/urls/).

2. Update `ordersys/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]
```

Remember that `app` is one of the supposedly many applications in this Django project, and `ordersys` is the "root" of
this project. So you may consider `ordersys/urls.py` as the root router of this project, and we need to
include `app.urls` here to wrap everything up.