from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, time
from pytz import timezone

from ..views import AutomationLogoutStockExchangesView, AutomationNotifyUserLoginView




# def start():
#     scheduler = BackgroundScheduler(timezone='Asia/Ho_Chi_Minh')

#     # Schedule the job to run once at 9:00 AM today
#     now = datetime.now()
#     run_time = datetime.combine(now.date(), time(9, 30, 0))

#     if now < run_time:
#         trigger_once = DateTrigger(
#             run_date=run_time, timezone='Asia/Ho_Chi_Minh')
#         scheduler.add_job(AutomationNotifyUserLoginView.notify_running, trigger=trigger_once,
#                           id="run_once_at_9", replace_existing=True)

#     # scheduler.start()
