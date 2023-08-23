from django.shortcuts import render
from operator import attrgetter
from account.models import Account
from kalendar.models import BlogPost

# Create your views here.

def home_screen_view(request):
    context = {}
    accounts = Account.objects.all()
    context['accounts'] = accounts

    events = sorted(BlogPost.objects.all(), key=attrgetter('event_date'), reverse=False)
    context['events'] =  events
    
    success_message_delete = request.session.pop('success_message_delete', None)
    context['success_message_delete'] = success_message_delete

    return render(request, "personal/home.html", context)

def version_view(request):
    return render(request, "personal/version.html")

def napoveda_view(request):
    return render(request, "personal/napoveda.html")