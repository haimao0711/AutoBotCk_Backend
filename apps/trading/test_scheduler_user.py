from django.contrib.auth import get_user_model
from apps.trading.scheduler.trading import start_scheduler_for_user
import logging

logger = logging.getLogger(__name__)

User = get_user_model()
username = "tranhaimao"

try:
    user = User.objects.get(username=username)
except User.DoesNotExist:
    logger.error(f"❌ User {username} không tồn tại trong DB!")
    raise

# Bật flag scheduler_status nếu chưa bật
if not user.scheduler_status:
    logger.info(f"🔧 Cập nhật scheduler_status=True cho user {username}")
    user.scheduler_status = True
    user.save()

# Khởi động scheduler cho user này
logger.info(f"🚀 Thử start_scheduler_for_user cho user {username}")
start_scheduler_for_user(user)
logger.info(f"✅ Hoàn tất start_scheduler_for_user cho user {username}")
