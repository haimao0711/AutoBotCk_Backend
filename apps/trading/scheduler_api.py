# APScheduler API endpoints đã được tắt - chỉ sử dụng Celery scheduler
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from .scheduler.trading import start_scheduler_for_user, stop_scheduler_for_user, get_scheduler_status_for_user

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def start_scheduler_user_api(request):
#     """API để bật Scheduler cho user đăng nhập"""
#     user = request.user  # Lấy user từ token
#     start_scheduler_for_user(user)
#     return Response({"message": f"Scheduler started for user {user.username}!"}, status=200)

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def stop_scheduler_user_api(request):
#     """API để dừng Scheduler của user đăng nhập"""
#     user = request.user  # Lấy user từ token
#     stop_scheduler_for_user(user)
#     return Response({"message": f"Scheduler stopped for user {user.username}!"}, status=200)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_scheduler_status_user_api(request):
#     """API để kiểm tra trạng thái Scheduler của user đăng nhập"""
#     user = request.user  # Lấy user từ token
#     status = get_scheduler_status_for_user(user)
#     return Response(status, status=200)
