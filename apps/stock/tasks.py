from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import close_old_connections
from .services import StockService
from .models import StockM1, StockM5, StockM15, StockH1, StockD1
from datetime import datetime, timedelta
import logging

logger = get_task_logger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_w1_task(self):
    """
    Celery task để download dữ liệu stock W1 (tuần)
    Chạy vào thứ 2 hàng tuần lúc 9:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download W1 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_w1()
        logger.info('Celery job download W1 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_w1_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_d1_task(self):
    """
    Celery task để download dữ liệu stock D1 (ngày)
    Chạy hàng ngày lúc 9:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download D1 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_d1()
        logger.info('Celery job download D1 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_d1_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_h1_task(self):
    """
    Celery task để download dữ liệu stock H1 (giờ)
    Chạy hàng giờ từ 9:00-15:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download H1 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_h1()
        logger.info('Celery job download H1 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_h1_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_m15_task(self):
    """
    Celery task để download dữ liệu stock M15 (15 phút)
    Chạy mỗi 15 phút từ 9:00-15:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download M15 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_m15()
        logger.info('Celery job download M15 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_m15_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_m5_task(self):
    """
    Celery task để download dữ liệu stock M5 (5 phút)
    Chạy mỗi 5 phút từ 9:00-15:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download M5 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_m5()
        logger.info('Celery job download M5 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_m5_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def download_stock_data_m1_task(self):
    """
    Celery task để download dữ liệu stock M1 (1 phút)
    Chạy mỗi phút từ 9:00-15:00
    """
    try:
        close_old_connections()
        logger.info('Celery job download M1 is running...')
        result = StockService.download_and_imported_data_to_datbase_chart_m1()
        logger.info('Celery job download M1 completed successfully')
        return result
    except Exception as exc:
        logger.error(f'Error in download_stock_data_m1_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def delete_old_stock_records_task(self):
    """
    Celery task để xóa các bản ghi stock cũ
    Chạy hàng giờ từ 9:00-15:00
    """
    try:
        close_old_connections()
        logger.info('Celery job delete old records is running...')
        
        # Định nghĩa chính sách lưu trữ cho mỗi model (số ngày)
        retention_policy = {
            StockM1: 5,     # 5 ngày
            StockM5: 7,     # 1 tuần
            StockM15: 7,    # 1 tuần
            StockH1: 14,    # 2 tuần
            StockD1: 60,    # 2 tháng (tạm tính là 60 ngày)
        }

        batch_size = 1000  # Số lượng bản ghi xóa mỗi lần
        logger.info("Bắt đầu xóa các bản ghi cũ...")

        for model, days in retention_policy.items():
            cutoff_datetime = datetime.now() - timedelta(days=days)
            cutoff_ts = int(cutoff_datetime.timestamp())
            model_name = model.__name__
            logger.info(f"Bắt đầu xóa các bản ghi cũ cho {model_name} (dữ liệu trước {cutoff_datetime})...")
            
            while True:
                # Lấy danh sách ID của các bản ghi cũ (theo cutoff_ts, giới hạn batch_size)
                old_records = model.objects.filter(time__lt=cutoff_ts).values_list('id', flat=True)[:batch_size]
                
                if not old_records:
                    break
                
                # Xóa các bản ghi cũ
                deleted_count = model.objects.filter(id__in=old_records).delete()[0]
                logger.info(f"Đã xóa {deleted_count} bản ghi cũ cho {model_name}")
                
                # Nếu số lượng xóa ít hơn batch_size, có nghĩa đã xóa hết
                if deleted_count < batch_size:
                    break
            
            logger.info(f"Hoàn thành xóa dữ liệu cũ cho {model_name}")
        
        logger.info('Celery job delete old records completed successfully')
        return True
        
    except Exception as exc:
        logger.error(f'Error in delete_old_stock_records_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()

@shared_task(bind=True, max_retries=3, default_retry_delay=300)
def sync_stocks_from_exchange_task(self):
    """
    Celery task để đồng bộ danh sách mã cổ phiếu từ sàn chứng khoán.
    Chạy định kỳ để cập nhật các mã mới niêm yết.
    """
    try:
        close_old_connections()
        logger.info('Celery job sync stocks from exchange is running...')
        result = StockService.sync_stocks_from_exchange()
        logger.info(f'Celery job sync stocks completed: {result}')
        return result
    except Exception as exc:
        logger.error(f'Error in sync_stocks_from_exchange_task: {exc}')
        raise self.retry(exc=exc)
    finally:
        close_old_connections()
