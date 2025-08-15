from django.db import models
from django.core.validators import MinValueValidator

from apps.account.detail.models import Account
from apps.authencation.user.models import User

import common.table_names as table

class UserAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.account}"

    class Meta:
        db_table = table.USER_ACCOUNT
