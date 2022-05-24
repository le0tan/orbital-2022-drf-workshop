## Django Rest Framework: The Basics

### Installation

```shell
pip install djangorestframework
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
```

### Setup

1. Add `'rest_framework'` to your `INSTALLED_APPS` setting (in `ordersys/settings.py`).

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

2. Add the browsable API to `ordersys/urls.py`

```python
from rest_framework import routers
from django.shortcuts import redirect

router = routers.DefaultRouter()

urlpatterns = [
    path('', lambda req: redirect('api/')),  # redirects the index URL to API root
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
```

3. (Temporary) set default authentication class to `BasicAuthentication` (in `settings.py`)

```python
# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
    ]
}
```

### Quick Demo

After the setup, you should be able to access the DRF browsable API at `localhost:8000/api/`, but it's useless for now
as we haven't add any API yet! While we we cover the how-to very soon, here's a very short demo on how easy it is to add
a new API:

```python
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework import routers, viewsets, serializers, permissions
from app.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]


router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', lambda req: redirect('api/')),  # redirects the index URL to API root
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
```

### Overview

There are three key concepts/components that you need to understand for this workshop:

1. **Serializers**: convert Django models (which is in Python object format) to API response (which is in JSON format),
   and vice versa.
2. **Viewsets**: a high-level abstraction provided by DRF that handles URL construction automatically based on common
   conventions, and leaves developers to focus on API behavior itself.
3. **Routers**: a utility used alongside **viewsets** that automatically wires URLs to corresponding views.

**NOTE:** If you refer to the DRF documentation, you'll realize that we skipped part 2 to 5 of the 6-part tutorial. Feel
free to read the documentation for more primitive usage of DRF,
and [the trade-offs between views and viewsets](https://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#trade-offs-between-views-vs-viewsets)
.

### Writing the API

1. Create new module `app/serializers`; create new file `course.py` for `CourseSerializer`.

```python
from rest_framework import serializers
from app.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
```

2. Create new module `app/apis`; create new file `course.py` for `CourseViewSet`.

```python
from rest_framework import viewsets, permissions
from app.models import Course
from app.serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]
```

3. Register `CourseViewSet` in the router (in `ordersys/urls.py`).

```python
from rest_framework import routers
from app.apis import CourseViewSet

router = routers.DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    ...
]
```

Now you have a fully functional REST API for the Course model! It supports CRUD and is authenticated by username and
password. It's easier than you thought, right?

## Django Rest Framework: Customization

We can follow the previous section to create REST APIs for other models, but only that would be too boring and trivial
wouldn't it? Let's look at some more advanced customization of DRF.

### Permission Management

Reference: [DRF Permissions](https://www.django-rest-framework.org/api-guide/permissions/#permissions)

In the definition of `CourseViewSet`, we have a line `permission_classes = [permissions.IsAuthenticated]` which uses
DRF's built-in permission class `IsAuthenticated`. As the name suggests, authenticated users will have full
permissions (i.e., read, change, delete) to the viewset. There are 6 other permissions provided by DRF:

* `AllowAny`: obvious...
* `IsAdminUser`: when `user.is_staff` is true (Only those with staff status can log into Django admin site)
* `IsAuthenticatedOrReadOnly`
* `DjangoModelPermissions`: follows Django's standard `django.contrib.auth` model permissions. This might be the most
  frequently used permissions for you.
* `DjangoModelPermissionsOrAnonReadOnly`: returns read-only view for non-authenticated user
* `DjangoObjectPermissions`: this thing is not officially supported by Django, and you need to learn about corresponding
  backend such as `django-guardian`, so we'll skip it for now (but we'll create our own object-level permission later).

#### Custom Permissions

Besides using built-in permissions, since DRF is an object-oriented framework, we can extend these permissions for our
own needs. There are two methods in a `Permission` class:

* `has_permission(self, request, view)` for model-level permission
* `has_object_permission(self, request, view, obj)` for object-level permission

For example, if you only want people to view, edit and add, but not delete `Table`, you can write the following custom
permission:

```python
from rest_framework import viewsets, permissions
from app.models import Table
from app.serializers import TableSerializer


class TablePermissions(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        if not super(TablePermissions, self).has_permission(request, view):
            return False
        if request.method in ["DELETE"]:
            return False
        return True


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [TablePermissions]
```

For example, if you don't know `DjangoModelPermissions` exists, you can still realize the same functionality by
extending `IsAuthenticated`:

```python
from rest_framework import viewsets, permissions
from app.models import Course
from app.serializers import CourseSerializer


class CoursePermissions(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        course = obj  # for better code competion in PyCharm
        if request.user.is_superuser:
            return True
        elif request.method in permissions.SAFE_METHODS:
            return request.user.has_perm('app.view_course')
        elif request.method == 'POST':
            return request.user.has_perm('app.add_course')
        elif request.method == 'PUT':
            return request.user.has_perm('app.change_course')
        elif request.method == 'DELETE':
            return request.user.has_perm('app.delete_course')
        return False


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [CoursePermissions]
```

### Customize Serializers

Ref: [DRF ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)
In our previous example, we included all fields by letting `fields = '__all__'` in the `Meta` class. We can do much
more:

1. Include a subset of fields

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
```

2. Exclude certain fields

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        exclude = ['users']
```

3. Nested serialization: if you look at the default response of `http://127.0.0.1:8000/api/orders/6/` you should see the
   following:

```json
{
  "id": 6,
  "date": "2022-05-17",
  "calling_number": 1,
  "status": "C",
  "table": 1
}
```

Here `table` is a foreign key field, however the details about this object is not serialized and only the primary
key `1` is shown here. Nested serialization means DRF will recursively serialize these objects up until `depth`. Below
is an example:

```python
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        depth = 1  # NEW
```

Then the response becomes:

```json
{
  "id": 6,
  "date": "2022-05-17",
  "calling_number": 1,
  "status": "C",
  "table": {
    "id": 1,
    "index": 1,
    "location": "Left"
  }
}
```

4. Specify read only fields

```python
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'account_name', 'users', 'created']
        read_only_fields = ['account_name']
```

There are many more customizations you can do to the `ModelSerializer`. If you have interest, you may refer to the DRF
documentation for more details.

### Filtering

Ref: [DRF Filtering](https://www.django-rest-framework.org/api-guide/filtering/)

For querying data, besides simply listing the objects (with or without pagination), DRF also supports filtering,
ordering and searching. You may specify the filter backend by setting `filter_backends` property of your viewset class.

* Filtering
    * backend: `django_filters.rest_framework.DjangoFilterBackend`
    * config: `filterset_fields = [...]`
* Ordering
    * backend: `rest_framework.filters.OrderingFilter`
    * config: `ordering_fields = [...]`
* Searching
    * backend: `rest_framework.filters.SearchFilter`
    * config: `search_fields = [...]`

Below are examples of applying these filters:

```python
from rest_framework import viewsets, permissions
from app.models import Order
from app.serializers import OrderSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permissions = [permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'table']
    ordering_fields = ['date']
```

```python
from rest_framework import viewsets, permissions, filters
from app.models import Table
from app.serializers import TableSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [TablePermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['location']
```

### Extra Actions

Ref: [DRF ViewSet Extra Actions](https://www.django-rest-framework.org/api-guide/viewsets/#marking-extra-actions-for-routing)

Of course your REST API can include custom functionality beyond CRUD on the models. To implement extra actions, you may
use `@action` decorator on top of your method.

Say you want to have an API `/orders/:id/deliver_order` that marks an order as delivered, you may write the following
method in `OrderViewSet`:

```python
from rest_framework import decorators, response


@decorators.action(detail=True, methods=['get'])
def deliver_order(self, request, pk=None):
    order = self.get_object()
    order.status = Order.STATUS_DELIVERED
    order.save()
    return response.Response({
        'status': 'ok',
        'order': OrderSerializer(order).data
    })
```

Here we set `detail=True` because this is an **object-level** method, which means this action is applicable only when we
have a specific object to work with. In this case, we can invoke `self.get_object()` method to fetch the current object.

Say you want to have an API `/orders/deliver_all_orders` that marks all orders as delivered, you may have the following:

```python
@decorators.action(detail=False, methods=['get'])
def deliver_all_orders(self, request):
    for order in Order.objects.all():
        order.status = Order.STATUS_DELIVERED
        order.save()
    return response.Response({
        'status': 'ok'
    })
```

Unlike the previous one, since we don't need a specific order to operate on, we set `detail=False` and this action works
on **model-level**.