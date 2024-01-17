from django.db import models

DAY_OF_THE_WEEK = {
    '1' : 'Monday',
    '2' : 'Tuesday',
    '3' : 'Wednesday',
    '4' : 'Thursday',
    '5' : 'Friday',
    '6' : 'Saturday', 
    '7' : 'Sunday',
}

class DayOfTheWeekField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['choices']=tuple(sorted(DAY_OF_THE_WEEK.items()))
        kwargs['max_length']=1 
        super(DayOfTheWeekField,self).__init__(*args, **kwargs)