# project/your_app/manage/user.py

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils import timezone

import hashlib
import secrets

from common.errors.messages import ErrorMessages

from ..role.enums import UserRoleEnum
from ..role.models import Role

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role=UserRoleEnum.USER, api_key=None):
        if not username:
            raise ValueError(ErrorMessages.USERS_MUST_HAVE_USERNAME)
        
        try:
            role_instance = Role.objects.get(name=role.value)
            
            if role is not UserRoleEnum.ADMIN and not api_key:
                api_key = self.generate_api_key()

            if role is UserRoleEnum.ADMIN:
                user = self.model(
                username=username,
                role=role_instance,
                api_key=api_key,
                created_by=None,
                created_at=timezone.now()
            )
            
            else:
                user = self.model(
                username=username,
                role=role_instance,
                api_key=api_key,
                created_by=None,
                created_at=timezone.now()
            )
                
            user.set_password(password)
            user.save(using=self._db)
            
            return user
        except (Role.DoesNotExist) as error:
            error_message = self.handle_error(error)
            raise ValidationError(error_message)

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password,
            role=UserRoleEnum.ADMIN
        )
        
        return user

    @staticmethod
    def generate_api_key():
        random_key = secrets.token_urlsafe(32)
        hashed_key = hashlib.sha256(random_key.encode()).hexdigest()

        return hashed_key
    
    @staticmethod
    def handle_error(error):
        error_messages = {
            Role.DoesNotExist: ErrorMessages.ROLE_DOES_NOT_EXIST
        }

        return error_messages.get(type(error), ErrorMessages.UNEXPECTED_ERROR)
