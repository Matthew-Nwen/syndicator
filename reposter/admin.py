from django.contrib import admin
from .models import event_post, event_toPost
import requests
import os
from syndicator.credentials import credentials

timezone = 'America/New_York'

# Register your models here.
def publish(modeladmin, request, querySet=event_toPost.objects.all()):
    # cache entry should be cleared for successful posting
    for event in querySet:
        publish_eventBrite(event)
        # publish_meetup(event)
        # publish_picatic(event.event)
        # publish_eventful(event.event)
publish.short_description = 'Repost selected events'

# This logic works!
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

# Unfortunately, couldn't test this with a free account...
def publish_meetup(event):
    headers = {
        'authorization': 'Bearer {0}'.format(credentials['mu_key'])
    }
    data = {
        'title': event.event_name,
        'description' : event.event_description,
        'duration': event.event_end_time - event.event_start_time,
        'group_id': credentials['mu_group'],
        'group_urlname': credentials['mu_group_url'],
        'guest_limit': 0,
        'hosts': credentials['mu_id'],
        'how_to_find_us': credentials['mu_find'],
        'name': event.event_name,
        'rsvp_limit': event.limit,
        'simple_html_description': event.event_description,
        'time': event.event_start_time,
        'venue_id': credentials['mu_venue_id'],
        'venue_visibility': 'public',
        'why': credentials['mu_why']
    }
    response = requests.post(
        'https://www.api.meetup.com/2/events/',
        headers = headers,
        data = data
    )
    return response.status_code == 201

# Ran into an oauth issue--the site uses an outdated oauth 1 schema.
def publish_eventful(event):
    headers = {
        'Authorization': 'Bearer {0}'.format(credentials['ef_key'])
    }
    data = {
        'app_key': credentials['ef_key'],
        'oauth_consumer_key': credentials['ef_okey'],
        'title': event.event_name,
        'start_time': event.event_start_time,
        'stop_time': event.event_end_time,
    }
    response = requests.post(
        'http://api.eventful.com/rest/events/new',
        headers = headers,
        data = data
    )
    print(response.content)

# Picatic immediately redirects my post requests--can't quite figure out
def publish_picatic(event):
    headers = {
        'Authorization': 'Bearer {0}'.format(credentials['pi_key'])
    }
    data = {
        'data': {
            'attributes': {
                'title': event.event_name,
            },
            'type': 'event'
        }
    }
    response = requests.get(
        'https://api.picatic.com/v2/event/',
        headers = headers,
        data = data,
    )
    return response.status_code == 201


class publishAdmin(admin.ModelAdmin):
    # list_display = ['event_name', 'reposted']
    # ordering = ['event_name']
    actions = [publish]

admin.site.register(event_toPost, publishAdmin)
admin.site.register(event_post)
