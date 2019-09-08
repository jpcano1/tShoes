# Django
from django.db import models

# Users Models
from users.models.users import User

class Designer(User, models.Model):
    """ Designer model """