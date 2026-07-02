from datetime import datetime, time
import pandas as pd
import math

from apps.configuration.details.models import Configuration
from apps.configuration.details.services import ConfigurationServices
from apps.trading.service.constants import DEFAULT_VALUE_PREVIOUS, DEFAULT_VALUE_CURRENT


# so sánh giá trị hiện tại so với tham chiếu của một thuộc tính
def is_valid_compare(value_attr: float, curr_attr: float, operator: str) -> bool:
    if operator == '<':
        return curr_attr <= value_attr
    elif operator == '>':
        return curr_attr >= value_attr
    else:
        return False

#kiểm tra xu hướng tăng hay giảm của một thuộc tính
def is_valid_trend(previous_attr: float, curr_attr: float, operator_trend: str) -> bool:
    if operator_trend in ['increase', '<']:
        return curr_attr > previous_attr
    elif operator_trend in ['decrease', '>']:
        return curr_attr < previous_attr
    else:
        return False

# kiểm tra xu hướng đảo chiều tăng hay giảm của một giả trị
def is_valid_trend_reserved(last_previous_value: float, previous_value: float, curr_value: float, operator_trend: str) -> bool:
    if operator_trend in ['increase', '<']:
        return last_previous_value >= previous_value and previous_value < curr_value
    elif operator_trend in ['decrease', '>']:
        return last_previous_value <= previous_value and previous_value > curr_value
    else:
        return False

# kiểm tra xu hướng đảo chiều tăng hay giảm của một thuộc tính
def is_valid_reversed_trend(pre_previous_attr: float, previous_attr: float, curr_attr: float, operator_trend: str) -> bool:
    if operator_trend in ['increase', '<']:
        return curr_attr > previous_attr and pre_previous_attr >= curr_attr
    elif operator_trend in ['decrease', '>']:
        return curr_attr < previous_attr and pre_previous_attr <= curr_attr
    else:
        return False


def render_new_from_keyword(keyword: str, key_update: str, importance_key: str) -> str:
    base_keyword = keyword.replace(importance_key, '').replace(
        'vnindex_config', f'vnindex_config_{key_update}').replace('stock_config', f'stock_config_{key_update}')

    return base_keyword


def get_is_valid_attr(config: Configuration, keyword: str, importance_key: str) -> bool:
    base_keyword = render_new_from_keyword(keyword, 'use', importance_key)
    is_valid_attr_name = base_keyword
    is_valid_attr = getattr(config, is_valid_attr_name, False)

    if 'vnindex' in base_keyword:
        return is_valid_attr and getattr(config, 'is_use_vnindex_config', False)
    elif 'stock' in base_keyword:
        return is_valid_attr and getattr(config, 'is_use_stock_config', False)
    else:
        return is_valid_attr

def get_valid_use_and_obl_fields(config: Configuration, config_type: str) -> list:
    # Lấy danh sách các field có tên chứa cả 'use' và 'obl'
    valid_fields = [
    field.name for field in Configuration._meta.fields
    if all(sub in field.name for sub in ('use', 'obl', config_type))
    ]

    # Chỉ giữ lại các field có giá trị True trong config
    return [field for field in valid_fields if getattr(config, field, False)]


def get_list_key_word_valid(config: Configuration, side_key: str, trend_key: str, importance_key: str, prefix: str) -> str:
    importance_key_condition_all_fields = [field.name for field in Configuration._meta.fields if field.name.endswith(
        importance_key) and (side_key in field.name or trend_key in field.name) and prefix in field.name]

    importance_key_condition_valid_all_fields = [
        field for field in importance_key_condition_all_fields
        if getattr(config, field, False)
    ]

    return [sufficient for sufficient in importance_key_condition_valid_all_fields if get_is_valid_attr(config, sufficient, importance_key)]


def get_last_previous_value_from_key(indicator_name: str, last_penultimate_data: pd.Series) -> float:
    if 'stoch_rsi' in indicator_name:
        return last_penultimate_data['stoch_rsi']
    elif 'rsi' in indicator_name:
        return last_penultimate_data['rsi']
    elif 'macd' in indicator_name:
        return last_penultimate_data['macd']
    elif 'histogram' in indicator_name:
        return last_penultimate_data['histogram']
    return 0

    # previous = get_previous_value_from_key(
    #         'stock_config', suff, config, stock_d1, stock_d0, '_sufficient_condition', side)

def get_previous_value_from_key(prefix: str, indicator_name: str, config: Configuration, penultimate_data: pd.Series, last_data: pd.Series, importance_key: str, side: str) -> float:
    if 'min_vnindex' in indicator_name and prefix in indicator_name:
        if side == 'buy':
            return config.vnindex_config_min_vnindex_buy
        else:
            return config.vnindex_config_min_vnindex_sell
    elif 'max_vnindex' in indicator_name and prefix in indicator_name:
        if side == 'buy':
            return config.vnindex_config_max_vnindex_buy
        else:
            return config.vnindex_config_max_vnindex_sell
    elif 'stoch_rsi' in indicator_name and prefix in indicator_name:
        if '_to' in indicator_name:
            base_keyword = render_new_from_keyword(
                indicator_name, 'value', importance_key)
            return getattr(config, base_keyword, 0.0)
        elif '_increase' in indicator_name or '_decrease' in indicator_name:
            return penultimate_data['stoch_rsi']
    elif 'rsi' in indicator_name and prefix in indicator_name:
        if '_to' in indicator_name:
            base_keyword = render_new_from_keyword(
                indicator_name, 'value', importance_key)
            return getattr(config, base_keyword, 0.0)
        elif '_increase' in indicator_name or '_decrease' in indicator_name:
            return penultimate_data['rsi']
    elif 'macd' in indicator_name and prefix in indicator_name:
        if '_to' in indicator_name:
            base_keyword = render_new_from_keyword(
                indicator_name, 'value', importance_key)
            return getattr(config, base_keyword, 0.0)
        elif '_increase' in indicator_name or '_decrease' in indicator_name:
            return penultimate_data['macd']
    elif 'sma' in indicator_name and prefix in indicator_name:
        if '_to' in indicator_name:
            base_keyword = render_new_from_keyword(
                indicator_name, 'value', importance_key)
            return getattr(config, base_keyword, 0.0)
        elif '_increase' in indicator_name or '_decrease' in indicator_name:
            return penultimate_data['sma']
    elif 'bolinger' in indicator_name and prefix in indicator_name:
        if side == 'buy':
            return last_data['lower_bolinger']
        else:
            return last_data['upper_bolinger']
    elif 'histogram' in indicator_name and prefix in indicator_name:
        return penultimate_data['histogram']
    elif 'volume' in indicator_name and prefix in indicator_name:
        return last_data['volume_ma']
    else:
        return DEFAULT_VALUE_PREVIOUS


def get_current_value_from_key(prefix: str, indicator_name: str, last_data: pd.Series) -> float:

    if 'min_vnindex' in indicator_name and prefix in indicator_name:
        return last_data['close']
    elif 'max_vnindex' in indicator_name and prefix in indicator_name:
        return last_data['close']
    elif 'stoch_rsi' in indicator_name and prefix in indicator_name:
        return last_data['stoch_rsi']
    elif 'rsi' in indicator_name and prefix in indicator_name:
        return last_data['rsi']
    elif 'macd' in indicator_name and prefix in indicator_name:
        return last_data['macd']
    elif 'sma' in indicator_name and prefix in indicator_name:
        return last_data['sma']
    elif 'bolinger' in indicator_name and prefix in indicator_name:
        return last_data['close']
    elif 'histogram' in indicator_name and prefix in indicator_name:
        return last_data['histogram']
    elif 'volume_trade' in indicator_name and prefix in indicator_name:
        return last_data.get('volume_trade', 0)
    elif 'volume' in indicator_name and prefix in indicator_name:
        return last_data['volume']
    # elif 'buy_up' in indicator_name and prefix in indicator_name:
    #     return last_data['buy_up']
    elif 'buy_foreign' in indicator_name and prefix in indicator_name:
        return last_data['buy_foreign']
    else:
        return DEFAULT_VALUE_CURRENT


def parse_time(time_str):
    return datetime.strptime(time_str, '%H:%M').time()


def is_within_time_range(start_time_str, end_time_str, current_time):
    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)

    return start_time <= current_time <= end_time


def round_up_to_unit(val1: float, val2: float, unit: float) -> float:
    average = (val1 + val2) / 2

    rounded_up = math.ceil(average / unit) * unit

    return rounded_up

def round_to_unit(value: float, unit: float) -> float:
    if unit == 0:
        return value
    return round(round(value / unit) * unit, 2)

def revert_status_request_trade(user, stock_id, reset_is_trading=True):
    from apps.configuration.details.overview.views import ConfigurationOverviewRequestViews
    from django.db import connection
    import time
    import logging
    logger = logging.getLogger(__name__)

    try:
        view_instance = ConfigurationOverviewRequestViews()
        view_instance.stop_request_trade(user, stock_id)
        if reset_is_trading:
            ConfigurationServices.update_is_trading_configuration(user, stock_id, False)
    except Exception as e:
        logger.error(f"Lỗi khi revert status request trade (Lần 1): {e}")
        connection.close()
        time.sleep(1)
        try:
            # Retry lần 2 sau khi reset connection
            view_instance = ConfigurationOverviewRequestViews()
            view_instance.stop_request_trade(user, stock_id)
            if reset_is_trading:
                ConfigurationServices.update_is_trading_configuration(user, stock_id, False)
        except Exception as retry_e:
             logger.error(f"Lỗi khi revert status request trade (Lần 2 - Thất bại): {retry_e}")
