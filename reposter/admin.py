from django.contrib import admin
from .models import event_post, event_toPost

# Register your models here.
def publish(modeladmin, request, querySet):
    # Here's where the reposting logic goes.
    # I'll have to figure out getting API keys
    # Then, it's as easy sending a bunch of postrequests for every cached entry
    # cache entry should be cleared for successful posting
    pass
publish.short_description = 'Trigger reposting events'

class publishAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'reposted']
    ordering = ['event_name']
    actions = [publish]

admin.site.register(event_post, publishAdmin)
admin.site.register(event_toPost)
