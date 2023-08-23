from django import template
from account.models import Account
from kalendar.models import BlogPost


register = template.Library()

@register.filter
def organizator_same_club(user, event_detail):
    if not user.is_authenticated:
        return False
    try:
        account = Account.objects.get(index=user.index)
        return account.is_admin or account.is_sekretar or account.is_organizator and user.club == event_detail.club
    except Account.DoesNotExist:
        return False

@register.filter    
def organizator_same_club_only(user, event_detail):
    try:
        account = Account.objects.get(index=user.index)
        return account.is_admin or account.is_organizator and user.club == event_detail.club
    except Account.DoesNotExist:
        return False
    

@register.filter
def get_event_description(event_code):
    event_dict = dict(BlogPost.event_type)
    return event_dict.get(event_code, 'Event description not found')
