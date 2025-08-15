from django.db import models

import common.table_names as table

from .enums import UserRoleEnum

class Role(models.Model):
    name = models.CharField(max_length=100)
    role_type = models.CharField(max_length=50, choices=[(role.name, role.value) for role in UserRoleEnum])

    def __str__(self):
        return self.name

    class Meta:
        db_table = table.ROLE
