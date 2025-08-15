from common.errors.messages import ErrorMessages
from .models import UserAccount
from apps.account.detail.services import AccountService
from apps.account.detail.models import Account

class UserAccountService:
    def check_account_belong_user(user, account):
        try:
            _ = UserAccount.objects.get(user=user,account=account)
            return True
        except UserAccount.DoesNotExist:
            return False
        
    def get_account_belong_user(user, account):
        try:
            user_account = UserAccount.objects.get(user=user,account=account)
            return user_account
        except UserAccount.DoesNotExist:
            raise ValueError(ErrorMessages.USER_DOES_NOT_HAVE_ACCOUNT)
        
    def get_accounts_belong_user(user):
        accounts = UserAccount.objects.filter(user=user)
        return accounts

    @staticmethod
    def create_user_account(user, account_name, account_num, password):
        """
        Tạo một tài khoản mới và liên kết với user, sử dụng thông tin từ request.
        """
        try:
            if not account_name or not account_num or not password:
                raise ValueError("Thiếu thông tin account_name, account_num hoặc password.")

            account = Account.objects.create(
                name=account_name,
                account_num=account_num,
                password=password  # Mã hóa password
            )

            # Liên kết tài khoản với user
            UserAccount.objects.create(user=user, account=account)

            return account
        except Exception as e:
            raise ValueError(f"Lỗi khi tạo tài khoản: {str(e)}")