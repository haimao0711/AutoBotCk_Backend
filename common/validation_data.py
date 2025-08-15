from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

chart_type_validator = RegexValidator(
    regex=r'^(following|trading|template)$',
    message='The type of chart should be following, trading or template only'
)

candle_type_validator = RegexValidator(
    regex=r'^(M1|M5|M15|H1|D1)$',
    message='Candle type must be one of M1, M5, M15, H1, D1'
)

BOT_STATUS_CHOICES = [
    ('waiting', 'Waiting'),
    ('running', 'Running'),
    ('finished', 'Finished'),
]

SIGNAL_TYPE_CHOICES = [
    ('buy', "Buy"),
    ('sell', "Sell")
]

bot_status_validator = RegexValidator(
    regex='^(waiting|running|finished)$',
    message='Value must be "waiting", "running", or "finished"',
    code='invalid_bot_status'
)

signal_type_validator = RegexValidator(
    regex=r'^(buy|sell)$',
    message='Signal type must be either "buy" or "sell"'
)


def validate_time_format(value):
    time_components = value.split(':')
    if len(time_components) != 2:
        raise ValidationError('Invalid time format. Use HH:MM.')

    try:
        hour = int(time_components[0])
        minute = int(time_components[1])
        if not (0 <= hour <= 23) or not (0 <= minute <= 59):
            raise ValueError
    except ValueError:
        raise ValidationError('Invalid time format. Use HH:MM.')
