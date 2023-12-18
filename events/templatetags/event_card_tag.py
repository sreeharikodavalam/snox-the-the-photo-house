from django import template

register = template.Library()


@register.inclusion_tag('../templates/event_card.html')
def render_event_card(event):
    return {'event': event}
