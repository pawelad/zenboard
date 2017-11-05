"""
webhook module signals
"""
import django.dispatch


github_event = django.dispatch.Signal(
    providing_args=['event', 'guid', 'payload'],
)


zenhub_event = django.dispatch.Signal(
    providing_args=['event', 'payload'],
)
