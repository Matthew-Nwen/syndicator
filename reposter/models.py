from django.db import models

# Create your models here.
class event_post(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.TextField('description of event')
    event_price = models.PositiveIntegerField('price of event')
    event_date = models.DateField('date of event')
    event_time = models.TimeField('time of event')
    event_duration = models.DurationField('duration of event')
