import pytz
import random
from typing import List
import pandas as pd
import numpy as np
from ta.trend import MACD
from ta.momentum import RSIIndicator
from datetime import datetime

from apps.telegram.sender import (send_message, send_message_telegram, define_message)
from apps.trading.enum.enums import ChartType
from apps.trading.service.utils import (get_current_value_from_key,
                                        get_last_previous_value_from_key, get_valid_use_and_obl_fields, get_list_key_word_valid, get_previous_value_from_key,
                                        is_valid_compare, is_valid_trend, is_valid_trend_reserved, is_within_time_range)
from apps.configuration.details.models import Configuration
from apps.trading.message import messages as MESSAGES
from common.signal.enums import SignalTelegramEnum
from apps.telegram.enum.enums import MessageTypeEnum

__all__ = [
    'round_to_nearest_hundred', 'append_messages_to_return', 'adding_idicator', 'send_telegram_message', 'render_type',
    'is_valid_vnindex_compare', 'is_valid_macd_compare', 'is_valid_stoch_rsi_compare', 'is_valid_rsi_compare', 'is_valid_volume_ma_compare',
    'is_valid_vnindex_trend', 'is_valid_macd_trend', 'is_valid_rsi_trend', 'is_valid_stoch_rsi_trend', 'is_valid_bolinger_trend', 'is_valid_histogram_trend'
]


def round_to_nearest_hundred(x):
    return round(x / 100) * 100


def append_messages_to_return(messages: List[str], base_message: str) -> str:
    for message in messages:
        base_message += message

    return base_message


def adding_idicator(df: pd.DataFrame):
    length_rsi = 14
    rsi = RSIIndicator(close=df["close"], window=length_rsi)
    rsi_values = rsi.rsi()
    df["rsi"] = rsi_values

    length_stoch = 14
    df['min_rsi'] = df['rsi'].rolling(window=length_stoch).min()
    df['max_rsi'] = df['rsi'].rolling(window=length_stoch).max()
  
    df['stoch_rsi_k'] = np.where(
        (df['max_rsi'] - df['min_rsi']) == 0, 
        0,  # Gán giá trị mặc định nếu mẫu số bằng 0
        100 * (df['rsi'] - df['min_rsi']) / (df['max_rsi'] - df['min_rsi'])
    )

    smoothK = 3
    smoothD = 3
    df['stoch_rsi_k_smooth'] = df['stoch_rsi_k'].rolling(window=smoothK).mean()
    df['stoch_rsi_d'] = df['stoch_rsi_k_smooth'].rolling(window=smoothD).mean()
    df["stoch_rsi"] = df['stoch_rsi_k_smooth']

    length_volume = 4
    df['volume_ma'] = df['volume'].rolling(window=length_volume).mean()

    macd = MACD(df["close"])
    df["macd"] = macd.macd()
    df["signal_line"] = macd.macd_signal()
    df['histogram'] = df['macd'] - df['signal_line']

    df['SMA'] = df['close'].rolling(window=20).mean()
    df['STD'] = df['close'].rolling(window=20).std()
    df['upper_bolinger'] = df['SMA'] + (df['STD'] * 2)
    df['lower_bolinger'] = df['SMA'] - (df['STD'] * 2)


# def send_telegram_message(user, message_type: MessageTypeEnum , status_signal: SignalTelegramEnum | None, **kwargs):
#     if isinstance(status_signal, SignalTelegramEnum):
#         send_message(user, message_type, status_signal.value, **kwargs)
#     else:
#         send_message(user, message_type, SignalTelegramEnum.DEFAULT.value, **kwargs)    

def send_telegram_message(user, message_type: MessageTypeEnum, status_signal: SignalTelegramEnum | None = None, **kwargs):
    try:
        # Kiểm tra biến đầu vào cơ bản
        if user is None or message_type is None:
            print("[Warning] send_telegram_message: user hoặc message_type bị thiếu, bỏ qua.")
            return  # Không làm gì, thoát hàm nhẹ nhàng

        # Xử lý status_signal hợp lệ
        if isinstance(status_signal, SignalTelegramEnum):
            send_message(user, message_type, status_signal.value, **kwargs)
        else:
            send_message(user, message_type, SignalTelegramEnum.DEFAULT.value, **kwargs)

    except Exception as e:
        # Chỉ log lỗi, không crash
        print(f"[Error] send_telegram_message gặp lỗi: {e}")


# def send_telegram_message_batch(user, message_type: MessageTypeEnum, batch_messages):
#     combined_message = ""  # Khởi tạo chuỗi để gộp nội dung
   
#     for message in batch_messages:
#         status_signal = message.get('status_signal')
#         message_kwargs = {key: value for key, value in message.items() if key != 'status_signal'}
#         # Xử lý chỉ khi có status_signal hợp lệ
#         if status_signal:
#             # Gọi hàm define_message để định dạng tin nhắn
#             formatted_message = define_message(status_signal.value, kwargs=message_kwargs)
#             # Thêm thông điệp định dạng vào chuỗi tổng hợp
#             combined_message += f"{formatted_message}"  # Ngăn cách giữa các tin nhắn để dễ đọc

#     # Gửi toàn bộ nội dung trong một tin nhắn duy nhất
#     print('check combined_message send telegram: ', combined_message)
#     send_message_telegram(user=user, message_type=message_type, message=combined_message)

def send_telegram_message_batch(user, message_type: MessageTypeEnum, batch_messages):
    try:
        # Kiểm tra đầu vào cơ bản
        if user is None or message_type is None:
            print("[Warning] send_telegram_message_batch: user hoặc message_type bị thiếu, bỏ qua.")
            return
        
        if not batch_messages or not isinstance(batch_messages, list):
            print("[Warning] send_telegram_message_batch: batch_messages rỗng hoặc không phải list, bỏ qua.")
            return

        combined_message = ""  # Khởi tạo chuỗi để gộp nội dung

        for message in batch_messages:
            try:
                status_signal = message.get('status_signal')
                message_kwargs = {key: value for key, value in message.items() if key != 'status_signal'}

                # Chỉ xử lý khi có status_signal hợp lệ
                if status_signal:
                    formatted_message = define_message(status_signal.value, kwargs=message_kwargs)
                    combined_message += f"{formatted_message}\n"  # Xuống dòng cho dễ đọc
            except Exception as e:
                print(f"[Error] Lỗi xử lý message {message}: {e}")
                continue  # Bỏ qua message lỗi, xử lý message tiếp theo

        # Gửi toàn bộ nội dung trong một tin nhắn duy nhất
        if combined_message:
            try:
                print('check combined_message send telegram: ', combined_message)
                send_message_telegram(user=user, message_type=message_type, message=combined_message)
            except Exception as e:
                print(f"[Error] Lỗi gửi telegram: {e}")
        else:
            print("[Info] Không có message hợp lệ để gửi telegram.")

    except Exception as e:
        print(f"[Error] send_telegram_message_batch gặp lỗi: {e}")



def render_type(chart_type: str, chart_value: str) -> str:
    match chart_type:
        case ChartType.Trading:
            return f'''
    **+ Cấu hình chart hành động** **{chart_value}:**'''
        case ChartType.Following:
            return f'''

    **+ Cấu hình chart theo dõi** **{chart_value}:**'''
        case _:
            return f'''

    *+ Cấu hình riêng cho tài khoản*'''


def is_valid_time_to_buy(config: Configuration):
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(timezone).time()
    is_use_time_to_buy = config.stock_config_is_use_time_to_buy
    start_time, end_time = config.stock_config_time_start_buy, config.stock_config_time_end_buy
    if is_use_time_to_buy:
        return is_within_time_range(start_time, end_time, now)
    else:
        return True

def is_valid_time_to_sell(config: Configuration):
    timezone = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(timezone).time()
    is_use_time_to_sell = config.stock_config_is_use_time_to_sell
    start_time, end_time = config.stock_config_time_start_sell, config.stock_config_time_end_sell
    if is_use_time_to_sell:
        return is_within_time_range(start_time, end_time, now)
    else:
        return True


def is_valid_vnindex_compare(value_vnindex_attr: float, curr_vnindex_attr: float, operator: str) -> bool:
    return is_valid_compare(value_vnindex_attr, curr_vnindex_attr, operator)


def is_valid_macd_compare(value_macd_attr: float, curr_macd_attr: float, operator: str) -> bool:
    return is_valid_compare(value_macd_attr, curr_macd_attr, operator)

def is_valid_buy_up_compare(value_macd_attr: float, curr_macd_attr: float, operator: str) -> bool:
    return is_valid_compare(value_macd_attr, curr_macd_attr, operator)

def is_valid_buy_foreign_compare(value_macd_attr: float, curr_macd_attr: float, operator: str) -> bool:
    return is_valid_compare(value_macd_attr, curr_macd_attr, operator)

def is_valid_volume_trade_compare(value_macd_attr: float, curr_macd_attr: float, operator: str) -> bool:
    return is_valid_compare(value_macd_attr, curr_macd_attr, operator)

def is_valid_stoch_rsi_compare(value_stoch_rsi_attr: float, curr_stoch_rsi_attr: float, operator: str) -> bool:
    return is_valid_compare(value_stoch_rsi_attr, curr_stoch_rsi_attr, operator)


def is_valid_rsi_compare(value_rsi_attr: float, curr_rsi_attr: float, operator: str) -> bool:
    return is_valid_compare(value_rsi_attr, curr_rsi_attr, operator)


def is_valid_volume_ma_compare(value_volume_ma_attr: float, curr_volume_ma_attr: float, operator: str) -> bool:
    return is_valid_compare(value_volume_ma_attr, curr_volume_ma_attr, operator)


def is_valid_vnindex_trend(previous_vnindex_attr: float, curr_vnindex_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_vnindex_attr, curr_vnindex_attr, operator_trend)


def is_valid_macd_trend(previous_macd_attr: float, curr_macd_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_macd_attr, curr_macd_attr, operator_trend)


def is_valid_rsi_trend(previous_rsi_attr: float, curr_rsi_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_rsi_attr, curr_rsi_attr, operator_trend)


def is_valid_stoch_rsi_trend(previous_stoch_rsi_attr: float, curr_stoch_rsi_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_stoch_rsi_attr, curr_stoch_rsi_attr, operator_trend)


def is_valid_bolinger_trend(previous_bolinger_attr: float, curr_bolinger_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_bolinger_attr, curr_bolinger_attr, operator_trend)


def is_valid_histogram_trend(previous_histogram_attr: float, curr_histogram_attr: float, operator_trend: str) -> bool:
    return is_valid_trend(previous_histogram_attr, curr_histogram_attr, operator_trend)


def is_valid_rsi_trend_reserved(d2_value: float, d1_value: float, d0_value: float, operator_trend: str) -> bool:
    return is_valid_trend_reserved(d2_value, d1_value, d0_value, operator_trend)


def is_valid_stoch_rsi_trend_reserved(d2_value: float, d1_value: float, d0_value: float, operator_trend: str) -> bool:
    return is_valid_trend_reserved(d2_value, d1_value, d0_value, operator_trend)


def is_valid_macd_trend_reserved(d2_value: float, d1_value: float, d0_value: float, operator_trend: str) -> bool:
    return is_valid_trend_reserved(d2_value, d1_value, d0_value, operator_trend)


def is_valid_histogram_trend_reserved(d2_value: float, d1_value: float, d0_value: float, operator_trend: str) -> bool:
    return is_valid_trend_reserved(d2_value, d1_value, d0_value, operator_trend)

sufficient_conditions = [
    'vnindex_config_min_vnindex_buy_sufficient_condition', 'vnindex_config_max_vnindex_buy_sufficient_condition',
    'vnindex_config_rsi_to_buy_sufficient_condition', 'vnindex_config_rsi_reversed_increase_sufficient_condition',
    'vnindex_config_stoch_rsi_to_buy_sufficient_condition', 'vnindex_config_stoch_rsi_reversed_increase_sufficient_condition',
    'vnindex_config_macd_to_buy_sufficient_condition', 'vnindex_config_macd_reversed_increase_sufficient_condition',
    'vnindex_config_histogram_reversed_increase_sufficient_condition', 'vnindex_config_volume_to_buy_sufficient_condition',
    'vnindex_config_bolinger_to_buy_sufficient_condition',

    # new adding to buy
    'vnindex_config_rsi_increase_sufficient_condition', 'vnindex_config_stoch_rsi_increase_sufficient_condition',
    'vnindex_config_macd_increase_sufficient_condition', 'vnindex_config_histogram_increase_sufficient_condition',

    'vnindex_config_min_vnindex_sell_sufficient_condition', 'vnindex_config_max_vnindex_sell_sufficient_condition',
    'vnindex_config_rsi_to_sell_sufficient_condition', 'vnindex_config_rsi_reversed_decrease_sufficient_condition',
    'vnindex_config_stoch_rsi_to_sell_sufficient_condition', 'vnindex_config_stoch_rsi_reversed_decrease_sufficient_condition',
    'vnindex_config_macd_to_sell_sufficient_condition', 'vnindex_config_macd_reversed_decrease_sufficient_condition',
    'vnindex_config_histogram_reversed_decrease_sufficient_condition', 'vnindex_config_volume_to_sell_sufficient_condition',
    'vnindex_config_bolinger_to_sell_sufficient_condition',

    # new adding to sell
    'vnindex_config_rsi_decrease_sufficient_condition', 'vnindex_config_stoch_rsi_decrease_sufficient_condition',
    'vnindex_config_macd_decrease_sufficient_condition', 'vnindex_config_histogram_decrease_sufficient_condition',

    'stock_config_min_stock_buy_sufficient_condition', 'stock_config_max_stock_buy_sufficient_condition',
    'stock_config_rsi_to_buy_sufficient_condition', 'stock_config_rsi_reversed_increase_sufficient_condition',
    'stock_config_stoch_rsi_to_buy_sufficient_condition', 'stock_config_stoch_rsi_reversed_increase_sufficient_condition',
    'stock_config_macd_to_buy_sufficient_condition', 'stock_config_macd_reversed_increase_sufficient_condition',
    'stock_config_histogram_reversed_increase_sufficient_condition', 'stock_config_volume_to_buy_sufficient_condition',
    'stock_config_bolinger_to_buy_sufficient_condition',

    # new adding to buy
    'stock_config_rsi_increase_sufficient_condition', 'stock_config_stoch_rsi_increase_sufficient_condition',
    'stock_config_macd_increase_sufficient_condition', 'stock_config_histogram_increase_sufficient_condition',

    'stock_config_min_stock_sell_sufficient_condition', 'stock_config_max_stock_sell_sufficient_condition',
    'stock_config_rsi_to_sell_sufficient_condition', 'stock_config_rsi_reversed_decrease_sufficient_condition',
    'stock_config_stoch_rsi_to_sell_sufficient_condition', 'stock_config_stoch_rsi_reversed_decrease_sufficient_condition',
    'stock_config_macd_to_sell_sufficient_condition', 'stock_config_macd_reversed_decrease_sufficient_condition',
    'stock_config_histogram_reversed_decrease_sufficient_condition', 'stock_config_volume_to_sell_sufficient_condition',
    'stock_config_bolinger_to_sell_sufficient_condition'

    # new adding to sell
    'stock_config_rsi_decrease_sufficient_condition', 'stock_config_stoch_rsi_decrease_sufficient_condition',
    'stock_config_macd_decrease_sufficient_condition', 'stock_config_histogram_decrease_sufficient_condition',
]

necessary_condition = [
    'vnindex_config_min_vnindex_buy_necessary_condition', 'vnindex_config_max_vnindex_buy_necessary_condition',
    'vnindex_config_rsi_to_buy_necessary_condition', 'vnindex_config_rsi_reversed_increase_necessary_condition',
    'vnindex_config_stoch_rsi_to_buy_necessary_condition', 'vnindex_config_stoch_rsi_reversed_increase_necessary_condition',
    'vnindex_config_macd_to_buy_necessary_condition', 'vnindex_config_macd_reversed_increase_necessary_condition',
    'vnindex_config_histogram_reversed_increase_necessary_condition', 'vnindex_config_volume_to_buy_necessary_condition',
    'vnindex_config_bolinger_to_buy_necessary_condition',

    # new adding to buy
    'vnindex_config_rsi_increase_necessary_condition', 'vnindex_config_stoch_rsi_increase_necessary_condition',
    'vnindex_config_macd_increase_necessary_condition', 'vnindex_config_histogram_increase_necessary_condition',

    'vnindex_config_min_vnindex_sell_necessary_condition', 'vnindex_config_max_vnindex_sell_necessary_condition',
    'vnindex_config_rsi_to_sell_necessary_condition', 'vnindex_config_rsi_reversed_decrease_necessary_condition',
    'vnindex_config_stoch_rsi_to_sell_necessary_condition', 'vnindex_config_stoch_rsi_reversed_decrease_necessary_condition',
    'vnindex_config_macd_to_sell_necessary_condition', 'vnindex_config_macd_reversed_decrease_necessary_condition',
    'vnindex_config_histogram_reversed_decrease_necessary_condition', 'vnindex_config_volume_to_sell_necessary_condition',
    'vnindex_config_bolinger_to_sell_necessary_condition',


    # new adding to sell
    'vnindex_config_rsi_decrease_necessary_condition', 'vnindex_config_stoch_rsi_decrease_necessary_condition',
    'vnindex_config_macd_decrease_necessary_condition', 'vnindex_config_histogram_decrease_necessary_condition',

    'stock_config_min_stock_buy_necessary_condition', 'stock_config_max_stock_buy_necessary_condition',
    'stock_config_rsi_to_buy_necessary_condition', 'stock_config_rsi_reversed_increase_necessary_condition',
    'stock_config_stoch_rsi_to_buy_necessary_condition', 'stock_config_stoch_rsi_reversed_increase_necessary_condition',
    'stock_config_macd_to_buy_necessary_condition', 'stock_config_macd_reversed_increase_necessary_condition',
    'stock_config_histogram_reversed_increase_necessary_condition', 'stock_config_volume_to_buy_necessary_condition',
    'stock_config_bolinger_to_buy_necessary_condition',

    # new adding to buy
    'stock_config_rsi_increase_necessary_condition', 'stock_config_stoch_rsi_increase_necessary_condition',
    'stock_config_macd_increase_necessary_condition', 'stock_config_histogram_increase_necessary_condition',

    'stock_config_min_stock_sell_necessary_condition', 'stock_config_max_stock_sell_necessary_condition',
    'stock_config_rsi_to_sell_necessary_condition', 'stock_config_rsi_reversed_decrease_necessary_condition',
    'stock_config_stoch_rsi_to_sell_necessary_condition', 'stock_config_stoch_rsi_reversed_decrease_necessary_condition',
    'stock_config_macd_to_sell_necessary_condition', 'stock_config_macd_reversed_decrease_necessary_condition',
    'stock_config_histogram_reversed_decrease_necessary_condition', 'stock_config_volume_to_sell_necessary_condition',
    'stock_config_bolinger_to_sell_necessary_condition'

    # new adding to sell
    'stock_config_rsi_decrease_necessary_condition', 'stock_config_stoch_rsi_decrease_necessary_condition',
    'stock_config_macd_decrease_necessary_condition', 'stock_config_histogram_decrease_necessary_condition',
]

keyword_to_function = {
    'min_vnindex': (is_valid_vnindex_compare, '>'),
    'max_vnindex': (is_valid_vnindex_compare, '<'),
    'rsi_to_buy': (is_valid_rsi_compare, '<'),
    'rsi_obl_to_buy': (is_valid_rsi_compare, '<'),
    'rsi_to_sell': (is_valid_rsi_compare, '>'),
    'rsi_reversed_increase': (is_valid_rsi_trend_reserved, 'increase'),
    'rsi_reversed_decrease': (is_valid_rsi_trend_reserved, 'decrease'),
    'stoch_rsi_to_buy': (is_valid_stoch_rsi_compare, '<'),
    'stoch_rsi_obl_to_buy': (is_valid_stoch_rsi_compare, '<'),
    'stoch_rsi_to_sell': (is_valid_stoch_rsi_compare, '>'),
    'stoch_rsi_reversed_increase': (is_valid_stoch_rsi_trend_reserved, 'increase'),
    'stoch_rsi_reversed_decrease': (is_valid_stoch_rsi_trend_reserved, 'decrease'),
    'macd_to_buy': (is_valid_macd_compare, '<'),
    'macd_obl_to_buy': (is_valid_macd_compare, '<'),
    'buy_up_obl_to_buy': (is_valid_buy_up_compare, '>'),
    'buy_foreign_obl_to_buy': (is_valid_buy_foreign_compare, '>'),
    'volume_trade_obl_to_buy': (is_valid_volume_trade_compare, '>'),
    'macd_to_sell': (is_valid_macd_compare, '>'),
    'macd_reversed_increase': (is_valid_macd_trend_reserved, 'increase'),
    'macd_reversed_decrease': (is_valid_macd_trend_reserved, 'decrease'),
    'histogram_reversed_increase': (is_valid_histogram_trend_reserved, 'increase'),
    'histogram_reversed_decrease': (is_valid_histogram_trend_reserved, 'decrease'),
    'volume_to_buy': (is_valid_compare, '<'),
    'volume_to_sell': (is_valid_compare, '>'),
    'bolinger_to_buy': (is_valid_bolinger_trend, 'increase'),
    'bolinger_to_sell': (is_valid_bolinger_trend, 'decrease'),
    'rsi_increase': (is_valid_rsi_trend, 'increase'),
    'rsi_decrease': (is_valid_rsi_trend, 'decrease'),
    'stoch_rsi_increase': (is_valid_stoch_rsi_trend, 'increase'),
    'stoch_rsi_decrease': (is_valid_stoch_rsi_trend, 'decrease'),
    'macd_increase': (is_valid_macd_trend, 'increase'),
    'macd_decrease': (is_valid_macd_trend, 'decrease'),
    'histogram_increase': (is_valid_histogram_trend, 'increase'),
    'histogram_decrease': (is_valid_histogram_trend, 'decrease'),
}


def handle_condition(condition_name: str, last_previous_value: float, previous_value: float, curr_value: float) -> bool:
    for keyword, (func, default_operator) in keyword_to_function.items():
        if keyword in condition_name:
            if 'reversed_increase' in condition_name or 'reversed_decrease' in condition_name:
                return func(last_previous_value, previous_value, curr_value, default_operator)
            else:
                return func(previous_value, curr_value, default_operator)


def should_do_obligatory(
    config: Configuration,
    data_df: pd.DataFrame,
    side: str,
    config_type: str
):
    obligatory_condition_valid_fields = get_valid_use_and_obl_fields(config, config_type)
    # print(f'check obligatory_condition_valid_fields {side}:', obligatory_condition_valid_fields)
    if len(obligatory_condition_valid_fields) == 0:
        return True, []

    d0 = data_df.iloc[-1]
    d1 = data_df.iloc[-2]
    d2 = data_df.iloc[-3]

    successed_reason = []
    for obl in obligatory_condition_valid_fields:
        if obl == "stock_config_use_buy_up_obl_to_buy":
         continue  # ❌ bỏ qua và tiếp tục obl tiếp theo
        number_decimal = 4 if 'histogram' in obl else 2
        key_obl_value =  obl.replace("use", "value")
        # print(f'check obl {obl}: ', obl)
        last_previous = round(get_last_previous_value_from_key(obl, d2), number_decimal)
        previous = round(getattr(config, key_obl_value, 0.0), number_decimal)
        current = round(get_current_value_from_key(config_type, obl, d0), number_decimal)
        # print(f'check current {obl}: ', current)
        # print(f'check previous {obl}: ', previous)
        if not handle_condition(obl, last_previous, previous, current):
            return False, [(obl, last_previous, previous, current)]
        else:
            successed_reason.append((obl, last_previous, previous, current))

    return True, successed_reason

def should_do_obligatory_trading(
    config: Configuration,
    data_df: pd.DataFrame,
    side: str,
    config_type: str
):
    obligatory_condition_valid_fields = get_valid_use_and_obl_fields(config, config_type)
    # print(f'check obligatory_condition_valid_fields {side}:', obligatory_condition_valid_fields)
    if len(obligatory_condition_valid_fields) == 0:
        return True, []

    d0 = data_df.iloc[-1]
    d1 = data_df.iloc[-2]
    d2 = data_df.iloc[-3]

    successed_reason = []
    for obl in obligatory_condition_valid_fields:
        if obl in ["stock_config_use_buy_up_obl_to_buy", "stock_config_use_buy_foreign_obl_to_buy" ] :
         continue  # ❌ bỏ qua và tiếp tục obl tiếp theo
        number_decimal = 4 if 'histogram' in obl else 2
        key_obl_value =  obl.replace("use", "value")
        # print(f'check obl {obl}: ', obl)
        last_previous = round(get_last_previous_value_from_key(obl, d2), number_decimal)
        previous = round(getattr(config, key_obl_value, 0.0), number_decimal)
        current = round(get_current_value_from_key(config_type, obl, d0), number_decimal)
        # print(f'check current {obl}: ', current)
        # print(f'check previous {obl}: ', previous)
        if not handle_condition(obl, last_previous, previous, current):
            return False, [(obl, last_previous, previous, current)]
        else:
            successed_reason.append((obl, last_previous, previous, current))

    return True, successed_reason

def should_do_sufficient(
    config: Configuration,
    data_df: pd.DataFrame,
    side: str,
    config_type: str
):
    trend_key = '_increase' if side == 'buy' else '_decrease'
    sufficient_condition_valid_fields = get_list_key_word_valid(
        config, side, trend_key, '_sufficient_condition', config_type)
    # print('check list sufficient_condition_valid_fields: ', sufficient_condition_valid_fields)

    if len(sufficient_condition_valid_fields) == 0:
        return False, []

    d0 = data_df.iloc[-1]
    d1 = data_df.iloc[-2]
    d2 = data_df.iloc[-3]

    failed_reason = []
    true_reason = []

    for suff in sufficient_condition_valid_fields:
        number_decimal = 4 if 'histogram' in suff else 2
        last_previous = round(get_last_previous_value_from_key(suff, d2), number_decimal)
        # print(f'check last_previous {suff}: ', last_previous)
        previous = round(get_previous_value_from_key(
            config_type, suff, config, d1, d0, '_sufficient_condition', side), number_decimal)
        # print(f'check previous {suff}: ', previous)
        current = round(get_current_value_from_key(config_type, suff, d0), number_decimal)
        # print(f'check current {suff}: ', current)
        if handle_condition(suff, last_previous, previous, current):
            true_reason.append((suff, last_previous, previous, current))
            return True, true_reason
        else:
            failed_reason.append((suff, last_previous, previous, current))

    return False, failed_reason


def should_do_necessary(
    config: Configuration,
    data_df: pd.DataFrame,
    side: str,
    config_type: str
):
    trend_key = '_increase' if side == 'buy' else '_decrease'
    necessary_condition_valid_fields = get_list_key_word_valid(
        config, side, trend_key, '_necessary_condition', config_type)
    # print('check list necessary_condition_valid_fields: ', necessary_condition_valid_fields)

    if len(necessary_condition_valid_fields) == 0:
        return False, []
    
    d0 = data_df.iloc[-1]
    d1 = data_df.iloc[-2]
    d2 = data_df.iloc[-3]

    successed_reason = []
    for suff in necessary_condition_valid_fields:
        number_decimal = 4 if 'histogram' in suff else 2
        last_previous = round(get_last_previous_value_from_key(suff, d2), number_decimal)
        previous = round(get_previous_value_from_key(
            config_type, suff, config, d1, d0, '_necessary_condition', side), number_decimal)
        current = round(get_current_value_from_key(
            config_type, suff, d0), number_decimal)
        if not handle_condition(suff, last_previous, previous, current):
            return False, [(suff, last_previous, previous, current)]
        else:
            successed_reason.append((suff, last_previous, previous, current))

    return True, successed_reason

def should_sell_sufficient(
        config: Configuration,
        vnindex_df: pd.DataFrame,
        stock_df: pd.DataFrame
):
    return should_do_sufficient(config, vnindex_df, stock_df, 'sell')


def should_sell_necessary(
    config: Configuration,
    vnindex_df: pd.DataFrame,
    stock_df: pd.DataFrame
):
    return should_do_necessary(config, vnindex_df, stock_df, 'sell')


def should_buy_chart(config: Configuration, data_df: pd.DataFrame, config_type: str):
    
    sufficient, s_reasons = should_do_sufficient(config, data_df, 'buy', config_type)
    necessary, n_reasons = should_do_necessary(config, data_df, 'buy', config_type)
    obligatory, o_reasons = should_do_obligatory(config, data_df, 'buy', config_type)
    # print('check sufficient: ', sufficient)
    # print('check obligatory: ', obligatory)
    # print('check o_reasons: ', o_reasons)
    if obligatory:
        if sufficient:
            return sufficient, {
                'obligatory': o_reasons,
                'sufficient': s_reasons}
        if necessary:
            return necessary, {
                'obligatory': o_reasons,
                'necessary': n_reasons}
        if not sufficient and not necessary:
            return False, {
                'sufficient': s_reasons,
                'necessary': n_reasons
            }
    else:
        return False, {
                'obligatory': o_reasons,
            }

def should_buy_chart_trading(config: Configuration, data_df: pd.DataFrame, config_type: str):
    
    sufficient, s_reasons = should_do_sufficient(config, data_df, 'buy', config_type)
    necessary, n_reasons = should_do_necessary(config, data_df, 'buy', config_type)
    obligatory, o_reasons = should_do_obligatory_trading(config, data_df, 'buy', config_type)
    if obligatory:
        if sufficient:
            return sufficient, {
                'obligatory': o_reasons,
                'sufficient': s_reasons}
        if necessary:
            return necessary, {
                'obligatory': o_reasons,
                'necessary': n_reasons}
        if not sufficient and not necessary:
            return False, {
                'sufficient': s_reasons,
                'necessary': n_reasons
            }
    else:
        return False, {
                'obligatory': o_reasons,
            }


def should_sell_chart(config: Configuration, data_df: pd.DataFrame, config_type: str):
    sufficient, s_reasons = should_do_sufficient(config, data_df, 'sell', config_type)
    necessary, n_reasons = should_do_necessary(config, data_df, 'sell', config_type)
    # print('check necessary: ', sufficient)
    # print('check n_reasons: ', n_reasons)
    if sufficient:
        return sufficient, {'sufficient': s_reasons}
    if necessary:
        return necessary, {'necessary': n_reasons}
    if not sufficient and not necessary:
        return False, {
            'sufficient': s_reasons,
            'necessary': n_reasons
        }


def  should_buy(
    trading_config: Configuration,
    following_config: Configuration,
    data_trading_df: pd.DataFrame,
    data_following_df: pd.DataFrame,
    config_type: str
):
    if is_valid_time_to_buy(trading_config):
        if not following_config.is_buy or not trading_config.is_buy:
            if not following_config.is_buy:
                return False, {
                    'following': {
                        'failed': {
                            'others': [('error_not_setup_buy_following_configuration', None, None, None)]
                        }
                    }
                }
            return False, {
                'trading': {
                    'failed': {
                        'others': [('error_not_setup_buy_trading_configuration', None, None, None)]
                    }
                }
            }
        obj_retured = {}
        # print('check following_config buy: ', following_config)
        # print('check trading_config buy: ', trading_config)
        following, following_reasons = should_buy_chart(
            following_config, data_following_df, config_type)

        trading, trading_reasons = should_buy_chart_trading(
            trading_config, data_trading_df, config_type )
        if not following:
            obj_retured['following'] = {
                'failed': following_reasons
            }
        else:
            obj_retured['following'] = {
                'success': following_reasons
            }
            if not trading:
                obj_retured['trading'] = {
                    'failed': trading_reasons
                }
            else:
                obj_retured['trading'] = {
                    'success': trading_reasons
                }
        # print('check following and trading: ', following and trading)
        # print('check obj_retured: ', obj_retured)
        return following,  following and trading, obj_retured

    else:
        return False, False, {
            'special_buy': {
                'failed':
                    {
                        'others': [('not_valid_time_to_buy', None, None, None)]
                    }
            }
        }

def  should_buy_following(
    following_config: Configuration,
    data_following_df: pd.DataFrame,
    config_type: str

):
    if not following_config.is_buy:
        return False, {
            'following': {
                'failed': {
                    'others': [('error_not_setup_buy_following_configuration', None, None, None)]
                }
            }
        }

    obj_retured = {}
    
    following, following_reasons = should_buy_chart(
        following_config, data_following_df, config_type)


    if not following:
        obj_retured['following'] = {
            'failed': following_reasons
        }
    else:
        obj_retured['following'] = {
            'success': following_reasons
        }

    return following , obj_retured



def  should_buy_trading(
    trading_config: Configuration,
    data_trading_df: pd.DataFrame,
    config_type: str
    ):   
    # if is_valid_time_to_buy(trading_config):
    if not trading_config.is_buy:
        return False, {
            'trading': {
                'failed': {
                    'others': [('error_not_setup_buy_following_configuration', None, None, None)]
                }
            }
        }

    obj_retured = {}
    
    trading, trading_reasons = should_buy_chart_trading(
        trading_config, data_trading_df, config_type)


    if not trading:
        obj_retured['trading'] = {
            'failed': trading_reasons
        }
    else:
        obj_retured['trading'] = {
            'success': trading_reasons
        }

    return trading , obj_retured

    # else:
    #     return False, {
    #         'special_buy': {
    #             'failed':
    #                 {
    #                     'others': [('not_valid_time_to_buy', None, None, None)]
    #                 }
    #         }
    #     }



def should_sell(
    trading_config: Configuration,
    following_config: Configuration,
    data_trading_df: pd.DataFrame,
    data_following_df: pd.DataFrame,
    config_type: str
):
    if is_valid_time_to_sell(trading_config):
        if not following_config.is_sell or not trading_config.is_sell:
            if not following_config.is_sell:
                return False, {
                    'following': {
                        'failed': {
                            'others': [('error_not_setup_buy_following_configuration', None, None, None)]
                        }
                    }
                }
            return False, {
                'trading': {
                    'failed': {
                        'others': [('error_not_setup_buy_trading_configuration', None, None, None)]
                    }
                }
            }
        obj_retured = {}
        following, following_reasons = should_sell_chart(
        following_config, data_following_df, config_type)
        trading, trading_reasons = should_sell_chart(
            trading_config, data_trading_df, config_type
        )
        if not following:
            obj_retured['following'] = {
                'failed': following_reasons
            }
        else:
            obj_retured['following'] = {
                'success': following_reasons
            }
            if not trading:
                obj_retured['trading'] = {
                    'failed': trading_reasons
                }
            else:
                obj_retured['trading'] = {
                    'success': trading_reasons
                }

        return following, following and trading, obj_retured

    else:
        return False, False, {
            'special_sell': {
                'failed':
                    {
                        'others': [('not_valid_time_to_sell', None, None, None)]
                    }
            }
        }

def  should_sell_trading(
    trading_config: Configuration,
    data_trading_df: pd.DataFrame,
    config_type: str

    ):   
    # if is_valid_time_to_sell(trading_config):
    if not trading_config.is_sell:
        return False, {
            'trading': {
                'failed': {
                    'others': [('error_not_setup_sell_following_configuration', None, None, None)]
                }
            }
        }

    obj_retured = {}
    
    trading, trading_reasons = should_sell_chart(
        trading_config, data_trading_df, config_type)


    if not trading:
        obj_retured['trading'] = {
            'failed': trading_reasons
        }
    else:
        obj_retured['trading'] = {
            'success': trading_reasons
        }
    print ('check trading: ', trading)
    print ('check obj_retured: ', obj_retured)
    return trading , obj_retured

    # else:
    #     return False, {
    #         'special_sell': {
    #             'failed':
    #                 {
    #                     'others': [('not_valid_time_to_sell', None, None, None)]
    #                 }
    #         }
    #     }

def should_sell_stop_loss(
    config: Configuration,    
):
    use_stop_loss_first_part = config.stock_config_use_stop_loss_first_part
    print('check use_stop_loss_first_part: ', use_stop_loss_first_part)
    percent_stop_loss_sell_first = config.stock_config_percent_stop_loss_sell_first
    print('check percent_stop_loss_sell_first: ', percent_stop_loss_sell_first)
    use_stop_loss_second_part = config.stock_config_use_stop_loss_second_part
    print('check use_stop_loss_second_part: ', use_stop_loss_second_part)
    percent_stop_loss_sell_second = config.stock_config_percent_stop_loss_sell_second
    print('check percent_stop_loss_sell_second: ', percent_stop_loss_sell_second)
    stop_loss_percent = config.stock_config_stop_loss_percent
    print('check stop_loss_percent: ', stop_loss_percent)

def should_sell_take_profit(
    config: Configuration,
    percentage_loss: float,
):
    use_take_profit_trigger = config.stock_config_use_take_profit_trigger
    take_profit_percent = config.stock_config_take_profit_percent
    use_take_profit_first_part = config.stock_config_use_take_profit_first_part
    percent_take_profit_sell_first = config.stock_config_percent_take_profit_sell_first
    percent_take_profit_sell_second = config.stock_config_percent_take_profit_sell_second
    stop_loss_percent = config.stock_config_stop_loss_percent

 #Kết quả chốt lời kiểu nào và phần trăm chốt lời
    is_take_profit = use_take_profit_trigger
    percent_profit = 1
    messages_take_profit = f'Mức lời hiện tại là {percentage_loss}% thỏa mãn mức yêu cầu chốt lãi là {take_profit_percent*100}%'

    if use_take_profit_first_part:
        is_take_profit = use_take_profit_first_part
        percent_profit = percent_take_profit_sell_second
        messages_take_profit = f'Mức lời hiện tại là {percentage_loss}% thỏa mãn mức yêu cầu chốt lãi là {percent_take_profit_sell_first*100}%'
    elif use_take_profit_trigger:
        if percentage_loss >= take_profit_percent:
            is_take_profit = use_take_profit_trigger
            percent_profit = 1
        else:
            is_take_profit = False
            # is_take_profit = use_take_profit_trigger  # nhớ xóa nó và mở dòng trên
            percent_profit = 1   
    return is_take_profit, percent_profit, messages_take_profit

def should_take_profit_bolinger(
    config: Configuration,
    price_current: float,
    upper_bolinger: float
):  
    is_take_profit = False
    use_bolinger_a_part_to_take_profit = config.stock_config_use_bolinger_a_part_to_take_profit
    percent_profit = 0
    messages_take_profit = f'Giá hiện tại: {price_current} >= bollinger trên: {upper_bolinger}'    
    if use_bolinger_a_part_to_take_profit:
        is_take_profit = use_bolinger_a_part_to_take_profit
        percent_profit = config.stock_config_percent_bolinger_a_part_to_take_profit
    return is_take_profit, percent_profit, messages_take_profit


def render_message(obj, trading_chart_value: str, following_chart_type: str):
    messages = ''
    for key, value in obj.items():
        if key == 'following':
            messages += render_type(ChartType.Following, following_chart_type)
            for f_key, f_value in value.items():
                if f_key == 'failed':
                    for f_failed_key, f_failed_value in f_value.items():
                        if f_failed_key == 'obligatory':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                        if f_failed_key == 'sufficient':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                        if f_failed_key == 'necessary':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                elif f_key == 'success':
                    for f_success_key, f_success_value in f_value.items():
                        if f_success_key == 'obligatory':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ✅'
                        if f_success_key == 'sufficient':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ✅'
                        if f_success_key == 'necessary':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages +=  message + ' ✅'
        if key == 'trading':
            messages += render_type(ChartType.Trading, trading_chart_value)
            for f_key, f_value in value.items():
                if f_key == 'failed':
                    for f_failed_key, f_failed_value in f_value.items():
                        if f_failed_key == 'obligatory':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                        if f_failed_key == 'sufficient':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                        if f_failed_key == 'necessary':
                            for key_word, last_previous, previous, current in f_failed_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ❌'
                elif f_key == 'success':
                    for f_success_key, f_success_value in f_value.items():
                        if f_success_key == 'obligatory':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ✅'
                        if f_success_key == 'sufficient':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ✅'
                        if f_success_key == 'necessary':
                            for key_word, last_previous, previous, current in f_success_value:
                                message_template = getattr(
                                    MESSAGES, key_word.upper())
                                message = message_template.format(
                                    previous=previous, current=current, old_previous=last_previous)
                                messages += message + ' ✅'
        if key == 'special_buy':
            message_template = getattr(
                MESSAGES, 'not_valid_time_to_buy'.upper())
            messages += message_template
        if key == 'special_sell':
            message_template = getattr(
                MESSAGES, 'not_valid_time_to_sell'.upper())
            messages += message_template

    return messages
