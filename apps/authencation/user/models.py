from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone 

from .manage import CustomUserManager
from ..role.models import Role

import common.table_names as table

class User(AbstractBaseUser):
    email = None
    username = models.CharField(max_length=100, unique=True)
    api_key = models.CharField(max_length=255, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    scheduler_status = models.BooleanField(default=False)
    telegram_bot_token = models.CharField(max_length=1000, blank=True, null=True)
    telegram_channel_id = models.CharField(max_length=1000, blank=True, null=True)
    telegram_bot_token_atc = models.CharField(max_length=1000, blank=True, null=True)
    telegram_channel_id_atc = models.CharField(max_length=1000, blank=True, null=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='create_user')
    created_at = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return f'User: {self.username}, Role: {self.role}'
    
    class Meta:
        db_table = table.USER
