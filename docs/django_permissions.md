When we initialized this Django project, we were already prompted to create a superuser. In Django, users are
represented with a special model named `User`. Here's an example of creating a new user via shell:

```python
>> > from django.contrib.auth.models import User
>> > user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

# At this point, user is a User object that has already been saved
# to the database. You can continue to change its attributes
# if you want to change other fields.
>> > user.last_name = 'Lennon'
>> > user.save()
```

There are two many-to-many fields of `User` related to permission management: `groups` and `user_permissions`. As
mentioned earlier, `User` is a model just like any other ones, so you can perform CRUD on these fields as shown below:

```python
myuser.groups.set([group_list])
myuser.groups.add(group, group, ...)
myuser.groups.remove(group, group, ...)
myuser.groups.clear()
myuser.user_permissions.set([permission_list])
myuser.user_permissions.add(permission, permission, ...)
myuser.user_permissions.remove(permission, permission, ...)
myuser.user_permissions.clear()
```

### Default Permissions

By default (if you followed the earlier instructions on creating the project and DB migration, and didn't mess up with
the boilerplate code) Django will create four `Permission`s for each model you migrated: add, change, delete and view.

For example, in our case, our application is named `app`, and our model is named `Course`, then you can check these four
permissions by:

* add: `user.has_perm('app.add_course')`
* change: `user.has_perm('app.change_course')`
* delete: `user.has_perm('app.delete_course')`
* view: `user.has_perm('app.view_course')`

### Custom Permissions

Besides the four default permissions for each model, you can also create custom permission as shown below:

```python
from app.models import Course
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Course)
permission = Permission.objects.create(
    codename='can_custom_ops',
    name='Can Perform Some Custom Operation',
    content_type=content_type,
)
```

**NOTE:** `ContentType` is basically a representation of models in your Django application. For more details, refer
to [the contenttypes framework](https://docs.djangoproject.com/en/4.0/ref/contrib/contenttypes/).

### Groups

A user in a group automatically has the permissions granted to that group. Here's an example:

```python
from django.contrib.auth.models import Group, Permission, User

# Create a group named staff
staff_group = Group(name='staff')
staff_group.save()

# Get the permission app.view_course and assign it to staff group
p = Permission.objects.get(content_type__app_label='app', codename='view_course')
staff_group.permissions.add(p)

# Assign myuser to the staff group
myuser = User.objects.get(username="myuser")
myuser.groups.add(staff_group)

# Check myuser has staff group's permissions
>> > myuser.has_perm("app.view_course")
True
```

For more details about Django authentication system,
read [here](https://docs.djangoproject.com/en/4.0/topics/auth/default/).