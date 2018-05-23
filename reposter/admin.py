from django.contrib import admin
from .models import event_post, event_toPost
import requests
import os
from syndicator.credentials import credentials

timezone = 'America/New_York'

# Register your models here.
def publish(modeladmin, request, querySet):
    # Here's where the reposting logic goes.
    # I'll have to figure out getting API keys
    # Then, it's as easy sending a bunch of postrequests for every cached entry
    # cache entry should be cleared for successful posting
    for event in event_toPost.objects.all():
        publish_eventBrite(event)
        
publish.short_description = 'Repost selected events'

def publish_eventBrite(event):
    data = {'event.name.html': event.event_name,
        "event.description.html": event.event_description,
        "event.start.timezone": timezone,
        "event.start.utc": event.event_start_time,
        "event.end.timezone": timezone,
        "event.end.utc": event.event_end_time,
        "event.currency": "USD",
    }
    headers = {'Authorization': "Bearer {0}".format(credentials['eb_key'])}
    response = requests.post(
        'https://www.eventbriteapi.com/v3/events/',
        headers = headers,
        data = data,
        verify = True,  # Verify SSL certificate
        allow_redirects = False,
    )
    if response.status_code == 200:
        id = str(response.json()['id'])
        eb_tickets = requests.post(
            'https://www.eventbriteapi.com/v3/events/'+id+'/ticket_classes/',
            headers = headers,
            data = {'ticket_class.name': 'General Admission',
                'ticket_class.donation': True,
            },
            verify = True,
        )
        print(eb_tickets.text)
        if eb_tickets.status_code != 200:
            return False
        eb_publish = requests.post(
            'https://www.eventbriteapi.com/v3/events/' + id + '/publish/',
            headers = headers,
            verify = True
        )
        return eb_publish.json()['published']
    return False

class publishAdmin(admin.ModelAdmin):
    # list_display = ['event_name', 'reposted']
    # ordering = ['event_name']
    actions = [publish]

admin.site.register(event_toPost, publishAdmin)
admin.site.register(event_post)
