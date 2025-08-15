def calculate_stoploss(stoploss_obj):

    stoploss, stoploss_percent, percent_volume_sell_stl = True, 0, 0
    stoploss = stoploss_obj['stock_config_use_stop_loss_first_part'] and stoploss_obj['stock_config_use_stop_loss_second_part']

    if stoploss:
        if stoploss_obj['stock_config_use_stop_loss_first_part']:
            percent_volume_sell_stl = 0.5 if not stoploss_obj[
                'stock_config_use_stop_loss_trigger'] else stoploss_obj['stock_config_stop_loss_percent']
            stoploss_percent = (
                1 - stoploss_obj['stock_config_percent_stop_loss_sell_first']) * percent_volume_sell_stl
        if stoploss_obj['stock_config_use_stop_loss_second_part']:
            percent_other_volume_sell_stl = 1 - percent_volume_sell_stl
            stoploss_percent += (
                1 - stoploss_obj['stock_config_percent_stop_loss_sell_second']) * percent_other_volume_sell_stl

    return stoploss, stoploss_percent


def calculate_profit(profit_obj):
    profit, profit_percent, percent_volume_sell_tp = True, 0, 0
    profit = profit_obj['stock_config_use_take_profit_first_part'] and profit_obj['stock_config_use_take_profit_second_part']

    if profit:
        if profit_obj['stock_config_use_take_profit_first_part']:
            percent_volume_sell_tp = 0.5 if not profit_obj[
                'stock_config_use_take_profit_trigger'] else profit_obj['stock_config_take_profit_percent']
            profit_percent = (
                1 + profit_obj['stock_config_percent_take_profit_sell_first']) * percent_volume_sell_tp
        if profit_obj['stock_config_use_take_profit_second_part']:
            percent_other_volume_sell_tp = 1 + percent_volume_sell_tp
            profit_percent += (
                1 + profit_obj['stock_config_percent_take_profit_sell_second']) * percent_other_volume_sell_tp

    return profit, profit_percent
