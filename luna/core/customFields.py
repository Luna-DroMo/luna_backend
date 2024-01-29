from django.db import models

DAY_OF_THE_WEEK = {
    '1': 'Monday',
    '2': 'Tuesday',
    '3': 'Wednesday',
    '4': 'Thursday',
    '5': 'Friday',
    '6': 'Saturday',
    '7': 'Sunday',
}


class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices'] = tuple(sorted(DAY_OF_THE_WEEK.items()))
        # Adjust based on the maximum expected length
        kwargs['max_length'] = 20
        super(DayOfTheWeekField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value:
            return value.split(',')
        return []

    def get_prep_value(self, value):
        if isinstance(value, list):
            return ','.join(value)
        return value

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)
