from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Role
from .serializers import RoleSerializer

from common.permissions.custom_permissions import RoleActionPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage


class UserRoleViews(APIView):
    serializers = RoleSerializer
    permission_classes = [RoleActionPermission]
    
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        role_type = request.data.get('role_type')
        role = Role.objects.get(role_type=role_type)
        serializer = RoleSerializer(Role, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        role_type = request.data.get('role_type')
        try:
            role = Role.objects.get(role_type=role_type)
            role.delete()
            return Response({'data': {'message': SuccessMessage.DELETE_ROLE_SUCCESSFUL}},status=status.HTTP_204_NO_CONTENT)
        except (Role.DoesNotExist):
            raise ValueError(ErrorMessages.ROLE_DOES_NOT_EXIST)
        