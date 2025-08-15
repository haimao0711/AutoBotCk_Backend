from rest_framework.permissions import BasePermission
from apps.authencation.role.enums import UserRoleEnum

class RegisterPermission(BasePermission):
    # def has_permission(self, request, view):
    #     return request.user.role.role_type == UserRoleEnum.ADMIN.value
    def has_permission(self, request, view):
        # Nếu là AnonymousUser, không kiểm tra role
        if not request.user or request.user.is_anonymous:
            return True  # Cho phép tiếp tục xử lý

        # Kiểm tra role của user
        return hasattr(request.user, "role") and request.user.role.role_type == UserRoleEnum.ADMIN.value
    
class RoleActionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == UserRoleEnum.ADMIN.value

class StockPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == UserRoleEnum.ADMIN.value
    
class ExchangeActionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == UserRoleEnum.ADMIN.value

class DownloadStockRequestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == UserRoleEnum.ADMIN.value

class UpdateAccountUserByPassPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.role_type == UserRoleEnum.ADMIN.value
