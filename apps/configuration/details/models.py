from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from ..candle.models import Candle
from ..type.models import ConfigurationType
from apps.authencation.user.models import User
from apps.account.detail.models import Account, SubAccount
from apps.stock.models import Stock

from common.validation_data import validate_time_format
import common.table_names as table


class Configuration(models.Model):
    # base infor
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, null=True)
    candle = models.ForeignKey(Candle, on_delete=models.CASCADE, null=True, related_name='configuration_buy_set')
    candle_sell = models.ForeignKey(Candle, on_delete=models.CASCADE, null=True, related_name='configuration_sell_set')
    config_type = models.ForeignKey(
        ConfigurationType, on_delete=models.CASCADE)
    level = models.IntegerField(default=6, validators=[
                                MinValueValidator(1), MaxValueValidator(6)])
    margin_percentage = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    # global config
    is_buy = models.BooleanField(default=True)
    is_sell = models.BooleanField(default=True)
    is_block_buy = models.BooleanField(default=False)
    is_block_sell = models.BooleanField(default=False)
    is_buy_hand = models.BooleanField(default=False)
    is_sell_hand = models.BooleanField(default=False)
    is_trading = models.BooleanField(default=False)
    is_use_vnindex_config = models.BooleanField(default=True)
    is_use_stock_config = models.BooleanField(default=True)

    # local config
    is_use_price_to_buy = models.BooleanField(default=False)
    price_to_buy_now = models.FloatField(
        default=0, validators=[MinValueValidator(0)])

    is_use_stoploss = models.BooleanField(default=False)
    percent_to_stoploss = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])

    is_use_takeprofit = models.BooleanField(default=False)
    percent_to_takeprofit = models.FloatField(
        default=0, validators=[MinValueValidator(0)])

    is_update_volume_buy = models.BooleanField(default=False)
    volume_to_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0)])
    last_time_use_buy_only_trading = models.DateTimeField(null=True)
    last_time_use_sell_only_trading = models.DateTimeField(null=True)

    ### ===================================================== VNINDEX_CONFIG ===================================================== ###

    #########################  BUYING   #########################

    # vnindex number

    vnindex_config_min_vnindex_buy = models.FloatField(
        default=20, validators=[MinValueValidator(0)])
    vnindex_config_max_vnindex_buy = models.FloatField(
        default=20, validators=[MinValueValidator(0)])

    vnindex_config_use_min_vnindex_buy = models.BooleanField(default=True)
    vnindex_config_use_max_vnindex_buy = models.BooleanField(default=True)

    vnindex_config_min_vnindex_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_min_vnindex_buy_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_max_vnindex_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_max_vnindex_buy_sufficient_condition = models.BooleanField(
        default=False)

    # rsi

    vnindex_config_use_rsi_to_buy = models.BooleanField(default=True)
    vnindex_config_use_rsi_obl_to_buy = models.BooleanField(default=False)
    vnindex_config_use_rsi_reversed_increase = models.BooleanField(
        default=True)
    vnindex_config_value_rsi_to_buy = models.FloatField(default=20, validators=[
        MinValueValidator(0), MaxValueValidator(100)])
    vnindex_config_value_rsi_obl_to_buy = models.FloatField(default=80, validators=[
        MinValueValidator(0), MaxValueValidator(100)])

    vnindex_config_rsi_to_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_to_buy_obligatory_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_rsi_increase = models.BooleanField(default=False)
    vnindex_config_rsi_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_increase_sufficient_condition = models.BooleanField(
        default=False)

    # stoch_rsi

    vnindex_config_use_stoch_rsi_to_buy = models.BooleanField(default=True)
    vnindex_config_use_stoch_rsi_obl_to_buy = models.BooleanField(default=True)
    vnindex_config_use_stoch_rsi_reversed_increase = models.BooleanField(
        default=True)
    vnindex_config_value_stoch_rsi_to_buy = models.FloatField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)])
    vnindex_config_value_stoch_rsi_obl_to_buy = models.FloatField(
        default=90, validators=[MinValueValidator(0), MaxValueValidator(100)])

    vnindex_config_stoch_rsi_to_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_to_buy_obligatory_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_stoch_rsi_increase = models.BooleanField(default=False)
    vnindex_config_stoch_rsi_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_increase_sufficient_condition = models.BooleanField(
        default=False)

    # macd
    vnindex_config_use_macd_to_buy = models.BooleanField(default=True)
    vnindex_config_use_histogram_to_buy = models.BooleanField(default=True)
    vnindex_config_use_macd_obl_to_buy = models.BooleanField(default=False)
    vnindex_config_use_histogram_obl_to_buy = models.BooleanField(default=False)
    vnindex_config_use_macd_reversed_increase = models.BooleanField(
        default=True)
    vnindex_config_value_macd_to_buy = models.FloatField(default=0)
    vnindex_config_value_histogram_to_buy = models.FloatField(default=0)
    vnindex_config_value_macd_obl_to_buy = models.FloatField(default=0)
    vnindex_config_value_histogram_obl_to_buy = models.FloatField(default=0)

    vnindex_config_macd_to_buy_necessary_condition = models.BooleanField(default=False)
    vnindex_config_histogram_to_buy_necessary_condition = models.BooleanField(default=False)
    vnindex_config_macd_to_buy_sufficient_condition = models.BooleanField(default=False)
    vnindex_config_histogram_to_buy_sufficient_condition = models.BooleanField(default=False)
    vnindex_config_macd_to_buy_obligatory_condition = models.BooleanField(default=False)
    vnindex_config_macd_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_macd_increase = models.BooleanField(default=False)
    vnindex_config_use_macd_obl_increase = models.BooleanField(default=False)
    vnindex_config_use_sma_increase = models.BooleanField(default=False)
    vnindex_config_use_sma_obl_increase = models.BooleanField(default=False)
    vnindex_config_macd_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_increase_sufficient_condition = models.BooleanField(
        default=False)

    # histogram
    vnindex_config_use_histogram_reversed_increase = models.BooleanField(
        default=True)
    vnindex_config_use_histogram_increase = models.BooleanField(
        default=True)

    vnindex_config_histogram_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_histogram_increase_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_increase_sufficient_condition = models.BooleanField(
        default=False)

    # volume_ma
    vnindex_config_use_volume_to_buy = models.BooleanField(default=True)

    vnindex_config_volume_to_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_volume_to_buy_sufficient_condition = models.BooleanField(
        default=False)

    # boilinger
    vnindex_config_use_bolinger_to_buy = models.BooleanField(default=True)

    vnindex_config_bolinger_to_buy_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_bolinger_to_buy_sufficient_condition = models.BooleanField(
        default=False)

    #########################  SELLING   #########################

    # vnindex

    vnindex_config_min_vnindex_sell = models.FloatField(
        default=20, validators=[MinValueValidator(0)])
    vnindex_config_max_vnindex_sell = models.FloatField(
        default=20, validators=[MinValueValidator(0)])
    vnindex_config_use_min_vnindex_sell = models.BooleanField(default=True)
    vnindex_config_use_max_vnindex_sell = models.BooleanField(default=True)

    vnindex_config_min_vnindex_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_min_vnindex_sell_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_max_vnindex_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_max_vnindex_sell_sufficient_condition = models.BooleanField(
        default=False)

    # rsi

    vnindex_config_use_rsi_to_sell = models.BooleanField(default=True)
    vnindex_config_use_rsi_reversed_decrease = models.BooleanField(
        default=True)
    vnindex_config_value_rsi_to_sell = models.FloatField(default=20, validators=[
        MinValueValidator(0), MaxValueValidator(100)])

    vnindex_config_rsi_to_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_rsi_decrease = models.BooleanField(default=False)
    vnindex_config_rsi_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_rsi_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # stoch_rsi
    vnindex_config_use_stoch_rsi_to_sell = models.BooleanField(default=True)
    vnindex_config_use_stoch_rsi_reversed_decrease = models.BooleanField(
        default=True)
    vnindex_config_value_stoch_rsi_to_sell = models.FloatField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)])

    vnindex_config_stoch_rsi_to_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_stoch_rsi_decrease = models.BooleanField(default=False)
    vnindex_config_stoch_rsi_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_stoch_rsi_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # macd
    vnindex_config_use_macd_to_sell = models.BooleanField(default=True)
    vnindex_config_use_histogram_to_sell = models.BooleanField(default=True)
    vnindex_config_use_macd_reversed_decrease = models.BooleanField(
        default=True)
    vnindex_config_value_macd_to_sell = models.FloatField(default=0)
    vnindex_config_value_histogram_to_sell = models.FloatField(default=0)
    vnindex_config_macd_to_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_to_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_use_macd_decrease = models.BooleanField(default=False)
    vnindex_config_macd_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_macd_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # histogram
    vnindex_config_use_histogram_reversed_decrease = models.BooleanField(
        default=True)
    vnindex_config_use_histogram_decrease = models.BooleanField(
        default=True)

    vnindex_config_histogram_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    vnindex_config_histogram_decrease_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_histogram_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # BOLINGER
    vnindex_config_use_bolinger_to_sell = models.BooleanField(default=True)

    vnindex_config_bolinger_to_sell_necessary_condition = models.BooleanField(
        default=False)
    vnindex_config_bolinger_to_sell_sufficient_condition = models.BooleanField(
        default=False)

    ### ===================================================== VNINDEX_CONFIG ===================================================== ###

    ### ========================================================================================================================== ###
    ### ========================================================================================================================== ###
    ### ========================================================================================================================== ###

    ### ===================================================== STOCKES_CONFIG ===================================================== ###

    # num_player

    stock_config_num_player = models.FloatField(
        default=1, validators=[MinValueValidator(1)])

    # rsi

    stock_config_use_rsi_to_buy = models.BooleanField(default=True)
    stock_config_use_rsi_obl_to_buy = models.BooleanField(default=True)
    stock_config_use_rsi_reversed_increase = models.BooleanField(default=True)
    stock_config_value_rsi_to_buy = models.FloatField(
        default=20, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock_config_value_rsi_obl_to_buy = models.FloatField(
        default=80, validators=[MinValueValidator(0), MaxValueValidator(100)])

    stock_config_rsi_to_buy_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_rsi_to_buy_obligatory_condition = models.BooleanField(
        default=False)
    stock_config_rsi_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_use_rsi_increase = models.BooleanField(default=False)
    stock_config_rsi_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_increase_sufficient_condition = models.BooleanField(
        default=False)

    # stoch_rsi

    stock_config_use_stoch_rsi_to_buy = models.BooleanField(default=True)
    stock_config_use_stoch_rsi_obl_to_buy = models.BooleanField(default=True)    
    stock_config_use_stoch_rsi_reversed_increase = models.BooleanField(
        default=True)
    stock_config_value_stoch_rsi_to_buy = models.FloatField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock_config_value_stoch_rsi_obl_to_buy = models.FloatField(
        default=80, validators=[MinValueValidator(0), MaxValueValidator(100)])    
    stock_config_stoch_rsi_to_buy_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_to_buy_obligatory_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_use_stoch_rsi_increase = models.BooleanField(default=False)
    stock_config_stoch_rsi_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_increase_sufficient_condition = models.BooleanField(
        default=False)

    # macd

    stock_config_use_macd_to_buy = models.BooleanField(default=True)
    stock_config_use_histogram_to_buy = models.BooleanField(default=True)
    stock_config_use_macd_obl_to_buy = models.BooleanField(default=True)
    stock_config_use_histogram_obl_to_buy = models.BooleanField(default=True)
    stock_config_use_macd_reversed_increase = models.BooleanField(default=True)
    stock_config_value_macd_to_buy = models.FloatField(default=0)
    stock_config_value_histogram_to_buy = models.FloatField(default=0)
    stock_config_value_macd_obl_to_buy = models.FloatField(default=0)
    stock_config_value_histogram_obl_to_buy = models.FloatField(default=0)

    stock_config_macd_to_buy_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_to_buy_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_histogram_to_buy_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_macd_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_macd_reversed_increase_obligatory_condition = models.BooleanField(
        default=False)

    stock_config_use_macd_increase = models.BooleanField(default=False)
    stock_config_use_macd_obl_increase = models.BooleanField(default=False)
    stock_config_use_sma_increase = models.BooleanField(default=False)
    stock_config_use_sma_obl_increase = models.BooleanField(default=False)
    stock_config_macd_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_increase_sufficient_condition = models.BooleanField(
        default=False)

    # histogram

    stock_config_use_histogram_reversed_increase = models.BooleanField(
        default=True)
    stock_config_use_histogram_increase = models.BooleanField(
        default=True)

    stock_config_histogram_reversed_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_reversed_increase_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_histogram_increase_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_increase_sufficient_condition = models.BooleanField(
        default=False)

    # volume

    stock_config_use_volume_to_buy = models.BooleanField(default=True)

    stock_config_volume_to_buy_necessary_condition = models.BooleanField(
        default=False)
    stock_config_volume_to_buy_sufficient_condition = models.BooleanField(
        default=False)

    # ========================================= SELLING =========================================

    # rsi
    stock_config_use_rsi_to_sell = models.BooleanField(default=True)
    stock_config_use_rsi_reversed_decrease = models.BooleanField(default=True)
    stock_config_value_rsi_to_sell = models.FloatField(
        default=20, validators=[MinValueValidator(0), MaxValueValidator(100)])

    stock_config_rsi_to_sell_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_rsi_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_use_rsi_decrease = models.BooleanField(default=False)
    stock_config_rsi_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_rsi_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # stoch_rsi
    stock_config_use_stoch_rsi_to_sell = models.BooleanField(default=True)
    stock_config_use_stoch_rsi_reversed_decrease = models.BooleanField(
        default=True)
    stock_config_value_stoch_rsi_to_sell = models.FloatField(
        default=30, validators=[MinValueValidator(0), MaxValueValidator(100)])

    stock_config_stoch_rsi_to_sell_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_use_stoch_rsi_decrease = models.BooleanField(default=False)
    stock_config_stoch_rsi_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_stoch_rsi_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # macd
    stock_config_use_macd_to_sell = models.BooleanField(default=True)
    stock_config_use_histogram_to_sell = models.BooleanField(default=True)
    stock_config_use_macd_reversed_decrease = models.BooleanField(default=True)
    stock_config_value_macd_to_sell = models.FloatField(default=0)
    stock_config_value_histogram_to_sell = models.FloatField(default=0)
    stock_config_macd_to_sell_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_to_sell_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_histogram_to_sell_sufficient_condition = models.BooleanField(
        default=False)
    stock_config_macd_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_use_macd_decrease = models.BooleanField(default=False)
    stock_config_macd_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_macd_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # histogram
    stock_config_use_histogram_reversed_decrease = models.BooleanField(
        default=True)
    stock_config_use_histogram_decrease = models.BooleanField(
        default=True)

    stock_config_histogram_reversed_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_reversed_decrease_sufficient_condition = models.BooleanField(
        default=False)

    stock_config_histogram_decrease_necessary_condition = models.BooleanField(
        default=False)
    stock_config_histogram_decrease_sufficient_condition = models.BooleanField(
        default=False)

    # ========================================= OTHER MODE =========================================
    # other mode
    stock_config_time_to_buy = models.FloatField(
        default=20, validators=[MinValueValidator(0)], null=True)
    stock_config_time_update_pid_buy = models.FloatField(
        default=5, validators=[MinValueValidator(0)], null=True)
    stock_config_is_mode_sensitive_buy = models.BooleanField(
        default=True, null=True)
    stock_config_percent_sensitive_buy = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_percent_first_buy = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_number_pid_buy_once_time = models.FloatField(
        default=3, validators=[MinValueValidator(0)], null=True)
    stock_config_percent_stock_buy_once_time = models.FloatField(
        default=0.2, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_slippage_volume_buy_per_pid = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_slippage_buy = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_add_price_buy = models.FloatField(
        default=0.2, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    # other mode
    stock_config_time_to_sell = models.FloatField(
        default=20, validators=[MinValueValidator(0)], null=True)
    stock_config_time_update_pid_sell = models.FloatField(
        default=5, validators=[MinValueValidator(0)], null=True)
    stock_config_is_mode_sensitive_sell = models.BooleanField(
        default=True, null=True)
    stock_config_percent_sensitive_sell = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_number_pid_sell_once_time = models.FloatField(
        default=3, validators=[MinValueValidator(0)], null=True)
    stock_config_percent_stock_sell_once_time = models.FloatField(
        default=0.2, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_slippage_volume_sell_per_pid = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_slippage_sell = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_add_price_sell = models.FloatField(
        default=0.2, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    # stop loss
    stock_config_use_stop_loss_first_part = models.BooleanField(
        default=True, null=True)
    stock_config_percent_stop_loss_sell_first = models.FloatField(
        default=0.03, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    stock_config_use_stop_loss_trigger = models.BooleanField(
        default=True, null=True)
    stock_config_stop_loss_percent = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    stock_config_use_stop_loss_second_part = models.BooleanField(default=True)
    stock_config_percent_stop_loss_sell_second = models.FloatField(
        default=0.03, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    # take profit
    stock_config_use_take_profit_first_part = models.BooleanField(
        default=True, null=True)
    stock_config_use_take_profit_first_part_two = models.BooleanField(
        default=True, null=True)
    stock_config_percent_take_profit_sell_first = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_percent_take_profit_sell_first_two = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_use_take_profit_trigger = models.BooleanField(
        default=True, null=True)
    stock_config_take_profit_percent = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)

    stock_config_use_take_profit_second_part = models.BooleanField(
        default=True, null=True)
    stock_config_use_take_profit_second_part_two = models.BooleanField(
        default=True, null=True)        
    stock_config_percent_take_profit_sell_second = models.FloatField(
        default=0.03, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_percent_take_profit_sell_second_two = models.FloatField(
        default=0.05, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_use_bolinger_to_take_profit = models.BooleanField(
        default=True, null=True)
    stock_config_use_bolinger_a_part_to_take_profit = models.BooleanField(
        default=True, null=True)
    stock_config_use_stoch_rsi_to_take_profit = models.BooleanField(default=True)
    stock_config_value_stoch_rsi_to_take_profit = models.FloatField(
        default=80, validators=[MinValueValidator(0), MaxValueValidator(100)])
    stock_config_percent_stoch_rsi_to_take_profit = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    stock_config_percent_bolinger_a_part_to_take_profit = models.FloatField(
        default=0.5, validators=[MinValueValidator(0), MaxValueValidator(1)], null=True)
    
    #buy up, sell down, buy foreign and sell foreign, volume_trade 
    stock_config_use_buy_up_obl_to_buy = models.BooleanField(default=False)
    stock_config_value_buy_up_obl_to_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])   
    stock_config_use_sell_down_obl_to_sell = models.BooleanField(default=False)
    stock_config_value_sell_down_obl_to_sell = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])  
    stock_config_use_buy_foreign_obl_to_buy = models.BooleanField(default=False)
    stock_config_value_buy_foreign_obl_to_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    stock_config_use_sell_foreign_obl_to_sell = models.BooleanField(default=False)
    stock_config_value_sell_foreign_obl_to_sell = models.FloatField(
        default=50, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    
    stock_config_use_volume_trade_obl_to_buy = models.BooleanField(default=False)
    stock_config_value_volume_trade_obl_to_buy = models.FloatField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]) 

    # advance mode
    stock_config_is_use_time_to_buy = models.BooleanField(
        default=False, null=True)
    stock_config_time_start_buy = models.TextField(
        default='09:30', validators=[validate_time_format], null=True)
    stock_config_time_end_buy = models.TextField(
        default='15:30', validators=[validate_time_format], null=True)
    stock_config_days_buy= models.CharField(
        default='12345',max_length=7, blank=True, null=True)

    stock_config_is_use_time_to_sell = models.BooleanField(
        default=False, null=True)
    stock_config_time_start_sell = models.TextField(
        default='09:30', validators=[validate_time_format], null=True)
    stock_config_time_end_sell = models.TextField(
        default='15:30', validators=[validate_time_format], null=True)
    stock_config_days_sell= models.CharField(
        default='12345',max_length=7, blank=True, null=True)

    #mandatory

    ### ===================================================== STOCKES_CONFIG ===================================================== ###

    class Meta:
        db_table = table.CONFIGURATION
        unique_together = ('user', 'stock', 'config_type')
