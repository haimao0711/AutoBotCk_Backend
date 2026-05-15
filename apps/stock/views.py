from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from apps.configuration.candle.enums import CandleEnum
from apps.stock.enums import DownloadStatusEnum
from apps.stock.models import StockD1, StockH1, StockM15, StockM5, StockM1
from apps.trading.service.helper import adding_idicator
from .services import DownloadService, StockService
from .models import Stock
from .serializers import StockSerializer

from common.permissions.custom_permissions import StockPermission, DownloadStockRequestPermission
from common.errors.messages import ErrorMessages
from common.success.messages import SuccessMessage
from datetime import datetime, timedelta
import time
from django.db import transaction
from django.db import close_old_connections
import logging
logger = logging.getLogger(__name__)

class StockViews(APIView):
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE']:
            return [StockPermission()]
        elif self.request.method in ['GET']:
            return []
        else:
            return []
    
    def get(self, request):
        search_key = request.query_params.get('key', None)
        limit = request.query_params.get('limit', None)
                
        if search_key:
            stocks = Stock.objects.filter(name__icontains=search_key)[:int(limit)] if limit else Stock.objects.filter(name__icontains=search_key)
        else:
            stocks = Stock.objects.all()[:int(limit)] if limit else Stock.objects.all()
            
        serializer = StockSerializer(stocks, many=True)
        
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StockSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        stock_name = request.data.get('name')
        stock = Stock.objects.get(name=stock_name)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        stock_name = request.data.get('name')
        try:
            stock = Stock.objects.get(name=stock_name)
            stock.delete()
            return Response({'data': {'message': SuccessMessage.DELETE_STOCK_SUCCESSFUL}},status=status.HTTP_204_NO_CONTENT)
        except (Stock.DoesNotExist):
            raise ValueError(ErrorMessages.STOCK_DOES_NOT_EXIST)
        
        
class StockImportedViews(APIView):
    permission_classes = [DownloadStockRequestPermission]

    @staticmethod
    def save_stock_data_w1():
        logger.info('job download w1 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_w1()
        except Exception as e:
            logger.warning(f"Error in job w1: {e}")
        finally:
            close_old_connections()

    @staticmethod
    def save_stock_data_d1():
        logger.info('job download d1 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_d1()
        except Exception as e:
            logger.warning(f"Error in job d1: {e}")
        finally:
            close_old_connections()

    @staticmethod
    def save_stock_data_h1():
        logger.info('job download h1 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_h1()
        except Exception as e:
            logger.warning(f"Error in job h1: {e}")
        finally:
            close_old_connections()

    @staticmethod
    def save_stock_data_m15():
        logger.info('job download m15 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_m15()
        except Exception as e:
            logger.warning(f"Error in job m15: {e}")
        finally:
            close_old_connections()

    @staticmethod
    def save_stock_data_m5():
        logger.info('job download m5 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_m5()
        except Exception as e:
            logger.warning(f"Error in job m5: {e}")
        finally:
            close_old_connections()

    @staticmethod
    def save_stock_data_m1():
        logger.info('job download m1 is running...')
        try:
            _ = StockService.download_and_imported_data_to_datbase_chart_m1()
        except Exception as e:
            logger.warning(f"Error in job m1: {e}")
        finally:
            close_old_connections()
    
    @staticmethod
    def delete_old_records():
        try:
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
                    old_record_ids = list(
                        model.objects.filter(time__lt=cutoff_ts)
                            .order_by('time')  # Xóa từ bản ghi cũ nhất
                            .values_list('id', flat=True)[:batch_size]
                    )

                    if not old_record_ids:
                        logger.info(f"Không còn bản ghi cũ để xóa cho {model_name}.")
                        break

                    try:
                        with transaction.atomic():  # Xóa an toàn trong một transaction
                            model.objects.filter(id__in=old_record_ids).delete()
                        logger.info(f"[{datetime.now()}] Đã xóa {len(old_record_ids)} bản ghi trong {model_name}.")
                    except Exception as e:
                        logger.warning(f"Lỗi khi xóa bản ghi trong {model_name}: {e}")
                        break  # Thoát vòng lặp nếu có lỗi

                    time.sleep(1)  # Delay để tránh tải nặng database

            logger.info("Hoàn thành xóa các bản ghi cũ.")
        except Exception as e:
            logger.error(f"Lỗi trong delete_old_records: {e}")
        finally:
            close_old_connections()
            
    def get(self, requests):
        try:
            stocks = StockService.get_stocks_for_configuration()
            stock_ids = [stock.id for stock in stocks]
            _ = StockService.download_imported_new_data_to_database_chart(stock_ids)
            return Response({'data': {'message': 'Start the endpoint for trigger download the data is successfully!'}}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in StockImportedViews.get: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            close_old_connections()

class DownloadStockView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            stock = StockService.get_stock_by_symbol('VNINDEX')
            data = DownloadService.download_data_single(stock, CandleEnum.D1, download_status=DownloadStatusEnum.NEW.value)
            adding_idicator(data)
            logger.info(data)
            return Response({
                "data": True
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in DownloadStockView.get: {e}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            close_old_connections()

class SetupStockSchedulesView(APIView):
    """
    API endpoint để setup Stock schedules vào Celery Beat database
    POST /api/stock/setup-schedules/
    """
    permission_classes = [StockPermission]
    
    def post(self, request):
        try:
            from apps.stock.scheduler.celery_scheduler import setup_stock_schedules
            
            logger.info('🔄 API request to setup stock schedules...')
            result = setup_stock_schedules()
            
            if result:
                return Response({
                    'success': True,
                    'message': '✅ Stock schedules setup completed successfully!',
                    'schedules': [
                        'delete_old_stock_records',
                        'download_stock_data_w1',
                        'download_stock_data_d1',
                        'download_stock_data_h1',
                        'download_stock_data_m15',
                        'download_stock_data_m5',
                        'download_stock_data_m1',
                        'sync_stocks_from_exchange'
                    ]
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'success': False,
                    'message': '❌ Failed to setup stock schedules'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            logger.error(f'Error setting up stock schedules: {e}')
            return Response({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SyncStockView(APIView):
    """
    API endpoint để đồng bộ danh sách mã cổ phiếu thủ công
    POST /api/stock/sync/
    """
    permission_classes = [StockPermission]
    
    def post(self, request):
        try:
            logger.info('🔄 API request to sync stocks from exchange...')
            result = StockService.sync_stocks_from_exchange()
            return Response({
                'success': True,
                'message': result
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f'Error syncing stocks: {e}')
            return Response({
                'success': False,
                'message': f'Error: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
