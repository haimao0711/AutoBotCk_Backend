from django.core.exceptions import ValidationError

from common.errors.messages import ErrorMessages
from apps.account.detail.enums import AccountLoginStatusEnum
from .models import Account, AccountType, SubAccount
from apps.account.user_account.models import UserAccount


class AccountService:
    def check_account_exist(account_id):
        try:
            _ = Account.objects.get(id=account_id)
            return True
        except Account.DoesNotExist:
            return False

    def check_account_exist_by_name(account_name):
        try:
            _ = Account.objects.get(name=account_name)
            return True
        except Account.DoesNotExist:
            return False

    def get_all_accounts():
        return Account.objects.all()

    def update_all_accounts_login_status():
        return Account.objects.filter(login_status=AccountLoginStatusEnum.LoginSuccess.value).update(login_status=AccountLoginStatusEnum.Logout.value, vps_session_id="")

    def get_account_by_id(account_id):
        try:
            account = Account.objects.get(id=account_id)
            return account
        except Account.DoesNotExist:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)

    def get_account_by_name(account_name):
        try:
            account = Account.objects.get(name=account_name)
            return account
        except Account.DoesNotExist:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)

    def get_accounts_by_ids(account_ids):
        accounts = Account.objects.filter(id__in=account_ids)
        return accounts

    def update_login_status_by_name(account_name, status):
        if status not in ['LoginSuccess', 'LoginFailed', 'Logout', 'NonActive']:
            return False, "Status is not exist"
        try:
            account = Account.objects.get(name=account_name)
            if account.status == status:
                return False, "Status is the same"
            account.status = status
            account.save()
        except Account.DoesNotExist:
            return False, "Account name is not exist"

    def get_account_type_by_name(name):
        try:
            return AccountType.objects.get(name=name)
        except AccountType.DoesNotExist:
            raise ValidationError(
                f'AccountType with name {name} does not exist')

    def validate_account_data_body(account_data):
        required_fields = {
            'amount': int,
            'valid': bool
        }

        for field, expected_type in required_fields.items():
            if field not in account_data:
                raise ValidationError(f'Missing required field: {field}')
            if not isinstance(account_data[field], expected_type):
                raise ValidationError(
                    f'Field {field} must be of type {expected_type.__name__}')

    def validate_account_data_partial_body(account_data):
        required_fields = {'amount', 'valid'}

        present_fields = set(account_data.keys())

        if not present_fields.issubset(required_fields):
            return False

        if not (len(present_fields) == 1 or len(present_fields) == 2):
            return False

        if 'amount' in present_fields:
            if not isinstance(account_data.get('amount'), (int, float)):
                return False

        if 'valid' in present_fields:
            if not isinstance(account_data.get('valid'), bool):
                return False

        return True

    def build_sub_account_naming(account_type: str, account_name: str):
        if account_type not in ['margin', 'normal']:
            return account_name
        elif account_type == 'margin':
            return account_name + '6'
        return account_name + '1'

    def get_subaccount_by_id(id: str) -> SubAccount | None:
        try:
            account = SubAccount.objects.get(id=id)
            return account
        except SubAccount.DoesNotExist:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)

    def get_subaccount_by_ids(account_ids):
        accounts = SubAccount.objects.filter(id__in=account_ids)
        return accounts

    def get_subaccount_by_name(name: str) -> SubAccount | None:
        try:
            account = SubAccount.objects.get(name=name)
            return account
        except SubAccount.DoesNotExist:
            raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)

    def check_subaccount_is_margin(account_type) -> bool:
        if account_type == 'Margin':
            return True
        return False
   
    @staticmethod
    def get_account_by_user(user):
        """
        Lấy tài khoản dựa theo user từ bảng UserAccount
        """
        try:
            user_account = UserAccount.objects.get(user=user)  # Lấy UserAccount
            return user_account.account  # Trả về Account liên kết
        except UserAccount.DoesNotExist:
            return None
    @staticmethod
    def get_account_by_name(user): 
        """
        Lấy tất cả tài khoản có cùng account.name với account của user truyền vào
        """
        try:
            # Lấy tài khoản của user truyền vào
            user_account = UserAccount.objects.get(user=user)
            account_name = user_account.account.name  # Lấy account.name

            # Lấy tất cả tài khoản có cùng account.name
            accounts = Account.objects.filter(name=account_name)

            return list(accounts)  # Trả về danh sách các account
        except UserAccount.DoesNotExist:
            return []