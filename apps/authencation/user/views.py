from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny

from apps.authencation.user.models import User
from ..role.models import Role
from ..role.enums import UserRoleEnum
from .serializers import UserLoginSerializer, UserSerializer

from config.settings import base as settings

from common.helper import init_api_key
from common.permissions.custom_permissions import RegisterPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage
from apps.account.detail.services import AccountService
from apps.account.user_account.services import UserAccountService
from apps.account.detail.serializers import AccountSerializer
import json
import re

class UserRegisterView(APIView):
    # permission_classes = [RegisterPermission, AllowAny]
    permission_classes = [AllowAny, RegisterPermission]
    def post(self, request):
        api_key = init_api_key()
        data = request.data.copy()
        data['api_key'] = api_key
        role = data.get('role')

        # Lấy thông tin Account từ request
        account_name = data.get('account_name')
        account_num = data.get('account_num')
        account_password = data.get('account_password')


        if role == UserRoleEnum.ADMIN.value:
            return Response({'error': ErrorMessages.REJECT_PERMISSION}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        try:
            user_role = Role.objects.get(name=role)
            data['role'] = user_role.id
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                validated_data = serializer.validated_data
                validated_data['password'] = make_password(validated_data['password'])
                user = serializer.save(api_key=api_key)

                # 🌟 **Tạo tài khoản giao dịch với thông tin từ request**
                try:
                    new_account = UserAccountService.create_user_account(
                        user=user,
                        account_name=account_name,
                        account_num=account_num,
                        password=account_password
                    )
                    print(f"Tài khoản {new_account.name} đã được tạo và liên kết với {user.username}")
                except Exception as acc_error:
                    print(f"Lỗi khi tạo tài khoản: {str(acc_error)}")
                    return JsonResponse({
                        'error': {'message': 'Lỗi khi tạo tài khoản'}
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return JsonResponse({
                    'data': {
                        'user': {
                            'id': user.id,
                            'username': user.username,
                        },
                        'account': {
                            'name': new_account.name,
                            'account_num': new_account.account_num
                        }
                    },
                    'message': SuccessMessage.REGISTER_SUCCESSFUL
                }, status=status.HTTP_201_CREATED)

            else:
                return JsonResponse({'error': {
                    'message': ErrorMessages.USERNAME_IS_ALREADY_EXIST,
                }}, status=status.HTTP_400_BAD_REQUEST)

        except Role.DoesNotExist:
            return ValidationError(ErrorMessages.ROLE_DOES_NOT_EXIST)


class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user  # người dùng hiện tại
        data = request.data.copy()
        old_password = data.get('old_password')
        new_password = data.get('new_password')

        # Kiểm tra đầu vào
        if not old_password or not new_password:
            return JsonResponse({'error': {'message': 'Cần cung cấp cả mật khẩu cũ và mật khẩu mới'}}, status=400)

        # Kiểm tra mật khẩu cũ
        if not user.check_password(old_password):
            return JsonResponse({'error': {'message': 'Mật khẩu cũ không đúng'}}, status=400)

        # Kiểm tra mật khẩu mới có khác mật khẩu cũ không
        if old_password == new_password:
            return JsonResponse({'error': {'message': 'Mật khẩu mới không thể giống mật khẩu cũ'}}, status=400)

        # Kiểm tra yêu cầu bảo mật của mật khẩu mới (ví dụ: dài ít nhất 8 ký tự, chứa chữ cái và số)
        if len(new_password) < 8 :
            return JsonResponse({'error': {'message': 'Mật khẩu mới phải có ít nhất 8 ký tự'}}, status=400)

        # Cập nhật mật khẩu mới
        user.set_password(new_password)
        user.save()

        # Cập nhật session của người dùng
        update_session_auth_hash(request, user)

        return JsonResponse({'data': {'message': 'Đổi mật khẩu thành công'}}, status=200)



class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        print('check data login: ', request.data)
        if serializer.is_valid():
            user = authenticate(
                request,
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                vps_account = AccountService.get_account_by_user(user)
                if not vps_account:
                     raise ValueError(ErrorMessages.ACCOUNT_DOES_NOT_EXIST)
                account_num = vps_account.account_num
                refresh = TokenObtainPairSerializer.get_token(user)
                data = {
                    'username': user.get_username(),
                    'user_role': user.role.role_type,
                    'user_id': user.id,
                    'vps_name': vps_account.name,
                    "vps_account": vps_account.account_num,
                    "vps_session_id": vps_account.vps_session_id,
                    'api_key': user.api_key if user.role.role_type != UserRoleEnum.ADMIN.value else None,
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    'access_expires': int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()),
                    'refresh_expires': int(settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds())
                }
                return Response(data, status=status.HTTP_200_OK)

        return Response({
            'message': ErrorMessages.LOGIN_FAILED,
        }, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(SuccessMessage.LOGOUT_SUCCESSFUL, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': {'message': str(e)}}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user
            body = json.loads(request.body.decode('utf-8')) if request.body else {}

            # Kiểm tra dữ liệu hợp lệ
            if not isinstance(body, dict):
                return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)

            # Lấy tài khoản của user
            vps_account = AccountService.get_account_by_user(user)
            if not vps_account:
                return Response({"error": "Account does not exist"}, status=status.HTTP_404_NOT_FOUND)

            # Lấy dữ liệu từ body
            limit_number_stocks = body.get("limit_number_stocks")
            limit_total_market_value = body.get("limit_total_market_value")
            account_password = body.get("account_password")
            # Kiểm tra xem tất cả các trường trong body có rỗng không
            if not any([limit_number_stocks, limit_total_market_value, account_password]):
                return Response({"error": "No fields provided to update"}, status=status.HTTP_400_BAD_REQUEST)

            # Tạo dictionary với các dữ liệu cần cập nhật
            vps_data_update = {}
            
            # Cập nhật các trường có trong payload
            if limit_number_stocks is not None and limit_number_stocks != 'null':  # Kiểm tra null string và None
                try:
                    limit_number_stocks = int(limit_number_stocks)  # Chuyển đổi sang integer nếu có thể
                    vps_data_update["limit_number_stocks"] = limit_number_stocks
                except ValueError:
                    return Response({"error": "Invalid value for limit_number_stocks, it must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            if limit_total_market_value is not None and limit_total_market_value != 'null':  # Kiểm tra null string và None
                try:
                    limit_total_market_value = int(limit_total_market_value)  # Chuyển đổi sang integer nếu có thể
                    vps_data_update["limit_total_market_value"] = limit_total_market_value
                except ValueError:
                    return Response({"error": "Invalid value for limit_total_market_value, it must be an integer."}, status=status.HTTP_400_BAD_REQUEST)
            # if account_password and account_password.strip().lower() != 'null':
            if account_password and account_password.strip() != 'd41d8cd98f00b204e9800998ecf8427e':
                vps_data_update["password"] = account_password

            print('check vps_data_update: ', vps_data_update)
            vps_serializer = AccountSerializer(vps_account, data=vps_data_update, partial=True)
            
            if vps_serializer.is_valid():
                vps_serializer.save()
            else:
                return Response({"error": vps_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

            # Trả về kết quả
            return Response({
                "data": {
                    "status": "success",
                    "account_name": vps_account.name,
                    "account_num": vps_account.account_num,
                    "limit_number_stocks": limit_number_stocks,
                    "limit_total_market_value": limit_total_market_value,
                }
            }, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            print("Error:", str(e))
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        