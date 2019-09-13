# Django
from django.db import models

# Users Models
from users.models.users import User


class Designer(User, models.Model):
    """ Designer model """
    
    def __str__(self):
        """ String function """
        return "Designer: {} with id: {}".format(self.first_name + " " + self.last_name, str(self.pk))
