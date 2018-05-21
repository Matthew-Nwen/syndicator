from django.db import models
from django.core.validators import MinValueValidator
from datetime import datetime

# Create your models here.
class event_post(models.Model):
    event_name = models.CharField(max_length=50)
    event_description = models.TextField('description of event')
    event_location = models.TextField('location of event', default='')
    event_price = models.DecimalField('price of event', decimal_places=2,
        max_digits=10, validators=[MinValueValidator(0)])
    event_date = models.DateField('date of event')
    event_start_time = models.TimeField('time of start of event', default=datetime.now)
    event_end_time = models.TimeField('time of end of event', default=datetime.now)
    reposted = models.BooleanField(default=False)

# Represents cached events that need to be posted.
# Should be stored in Redis or Memcached
class event_toPost(models.Model):
    event = models.OneToOneField(event_post, on_delete='PROTECT')
