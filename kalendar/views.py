import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.utils.text import slugify
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.urls import reverse

from openpyxl import Workbook


from kalendar.models import BlogPost, EventEntry, MicroEvent, MicroEventEntry
from kalendar.forms import CreateEventForm, UpdateEventForm, EventEntryForm, CreateMicroEventForm, MicroEventEntryForm
from account.forms import Account
from account.models import Account
from .templatetags.account_tags import organizator_same_club, organizator_same_club_only







def create_kalendar_view(request):

    context = {}

    user = request.user
    if not user.is_authenticated or not user.is_organizator:
        return redirect('must_authenticate')        
    
    form = CreateEventForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        author = Account.objects.filter(email=user.email).first()
        obj.author = author
        obj.club = author.club
        obj.save()
        form = CreateEventForm()
        request.session['success_message_create'] = "Událost byla úspěšně vytvořena"

        return HttpResponseRedirect(reverse('kalendar:event', args=[obj.slug]))

    context['form'] = form

    return render(request, "kalendar/event_create.html", {} )


def event_detail_view(request, slug, microevent_id=None):

    context = {}

    event_detail = get_object_or_404(BlogPost, slug=slug)
    num_joined_users = EventEntry.objects.filter(event=event_detail).count()
    entries = event_detail.evententry_set.order_by('category') 
    user_has_entry = False


    if request.user.is_authenticated:
        try:
            user_entry = EventEntry.objects.get(event=event_detail, index=request.user.index)
            user_has_entry = True
        except EventEntry.DoesNotExist:
            pass

    current_time = timezone.now()

    if event_detail.termin_prihl <= current_time:
        message = "Přihlašování uzavřeno"
    else:
        message = None

    if request.user.is_authenticated:
        try:
            user_entry = EventEntry.objects.get(event=event_detail, index=request.user.index)
            user_has_entry = True
        except EventEntry.DoesNotExist:
            pass

    current_time = timezone.now()

    if event_detail.termin_prihl <= current_time:
        message = "Přihlašování uzavřeno"
    else:
        message = None


    microevent_form = CreateMicroEventForm()
    microevent_entry_form = MicroEventEntryForm()
    message_you_can_not_enter = ""

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            microevent_form = CreateMicroEventForm(request.POST)
            if microevent_form.is_valid():
                microevent = microevent_form.save(commit=False)
                microevent.main_event = event_detail
                microevent.save()

                max_entries = microevent_form.cleaned_data['max_entries']
                microevent.max_entries = max_entries
                microevent.save()

                request.session['success_message_create_microevent'] = "Auto úspěšně přidáno"
                return redirect('kalendar:event', slug=slug)
            
        elif action == 'enter':
            microevent_id = request.POST.get('microevent_id')
            selected_microevent = get_object_or_404(MicroEvent, id=microevent_id)

            # Check if entry limit is reached
            if selected_microevent.microevententry_set.count() >= selected_microevent.max_entries:
                message_you_can_not_enter = "Již nejsou volná místa v autě"
            else:
                microevent_entry_form = MicroEventEntryForm(request.POST, initial={'microevent': selected_microevent.id})
                if microevent_entry_form.is_valid():
                    microevent_entry = microevent_entry_form.save(commit=False)
                    microevent_entry.microevent = selected_microevent
                    microevent_entry.save()
                    request.session['success_message_create_microevent'] = "Přidal jsi se úspěšně do auta"
                    return redirect('kalendar:event', slug=slug)
        
        elif action == 'save_entry':
            microevent_id = request.POST.get('microevent_id')
            entry_id = request.POST.get('entry_id')
            microevent = get_object_or_404(MicroEvent, id=microevent_id)
            entry = get_object_or_404(MicroEventEntry, id=entry_id)

            entry.name = request.POST.get(f'entry_name_{entry_id}')
            entry.notice_name = request.POST.get(f'entry_notice_name_{entry_id}')
            entry.save()
            request.session['success_message_save_entry'] = "Změny v autě byly úspěšně uloženy"
            return redirect('kalendar:event', slug=slug)
        
        elif action == 'save_notice':
            microevent_id = request.POST.get('microevent_id')
            new_notice = request.POST.get('notice')
            microevent = get_object_or_404(MicroEvent, id=microevent_id)
            microevent.notice = new_notice
            microevent.save()
            request.session['success_message_save_notice'] = "Poznámka k autu úspěšně uložena"
            return redirect('kalendar:event', slug=slug)
            
        elif action == 'delete':
            # Handle microevent deletion
            microevent_id = request.POST.get('microevent_id')
            microevent = get_object_or_404(MicroEvent, id=microevent_id)
            microevent.delete()
            request.session['success_message_microevent_delete'] = "Auto úspěšně smazáno"
            return redirect('kalendar:event', slug=slug)
    else:
        microevent_form = CreateMicroEventForm()
        microevent_entry_form = MicroEventEntryForm()

    # Fetch list of created microevents
    microevents = MicroEvent.objects.filter(main_event=event_detail)


        


    context['microevents'] = microevents
    context['microevent_entry_form'] = microevent_entry_form
    context['microevent_form'] = microevent_form
    context['message_you_can_not_enter'] = message_you_can_not_enter    
    context['success_message_create_microevent'] = request.session.pop('success_message_create_microevent', None)
    context['success_message_microevent_delete'] = request.session.pop('success_message_microevent_delete', None)
    context['success_message_save_entry'] = request.session.pop('success_message_save_entry', None)
    context['success_message_save_notice'] = request.session.pop('success_message_save_notice', None)
    




    
    success_message_create = request.session.pop('success_message_create', None)
    success_message_edit = request.session.pop('success_message_update', None)
    success_message_entry = request.session.pop('success_message_entry', None)
    success_message_entry_delete = request.session.pop('success_message_entry_delete', None)
    success_message_entry_cantupdate = request.session.pop('success_message_entry_cantupdate', None)
    success_message_entry_update = request.session.pop('success_message_entry_update', None)
    success_message_entries_update = request.session.pop('success_message_entries_update', None)
    success_message_entries_cantupdate = request.session.pop('success_message_entries_cantupdate', None)
    success_message_entries_delete = request.session.pop('success_message_entries_delete', None)
    success_message_new_from_entries = request.session.pop('success_message_new_from_entries', None)


    context['event_detail'] = event_detail
    context['user_has_entry'] = user_has_entry
    context['num_joined_users'] = num_joined_users
    context['entries'] = entries
    context['event_club'] = event_detail.club
    context['message'] = message
    context['success_message_create'] = success_message_create
    context['success_message_update'] = success_message_edit
    context['success_message_entry'] = success_message_entry
    context['success_message_entry_delete'] = success_message_entry_delete
    context['success_message_entry_cantupdate'] = success_message_entry_cantupdate
    context['success_message_entry_update'] = success_message_entry_update
    context['success_message_entries_update'] = success_message_entries_update
    context['success_message_entries_cantupdate'] = success_message_entries_cantupdate
    context['success_message_entries_delete'] = success_message_entries_delete
    context['success_message_new_from_entries'] = success_message_new_from_entries




    return render(request, 'kalendar/event_detail.html', context)







def event_edit_view(request, slug):

    context = {}

    user = request.user
    event_detail = get_object_or_404(BlogPost, slug=slug)

    if not user.is_authenticated or not organizator_same_club(user, event_detail):
        return redirect('must_authenticate')
    
    if request.POST:
        # Check if the "Delete Event" button was clicked
        if 'event_delete' in request.POST:
            # Delete the event and related files
            event_detail.bulletin.delete()
            event_detail.pokyny.delete()
            event_detail.startlist.delete()
            event_detail.results.delete()
            event_detail.splittimes.delete()
            event_detail.mapa.delete()
            event_detail.delete()

            request.session['success_message_delete'] = "Událost úspěšně smazána"   

            return redirect('home')  # Redirect to a list of events after deletion
        
        form = UpdateEventForm(request.POST or None, request.FILES or None, instance=event_detail)
        if form.is_valid():
            if form.cleaned_data['delete_bulletin']:
                event_detail.bulletin.delete()
            if form.cleaned_data['delete_pokyny']:
                event_detail.pokyny.delete()
            if form.cleaned_data['delete_startlist']:
                event_detail.startlist.delete()
            if form.cleaned_data['delete_results']:
                event_detail.results.delete()
            if form.cleaned_data['delete_splittimes']:
                event_detail.splittimes.delete()
            if form.cleaned_data['delete_mapa']:
                event_detail.mapa.delete()
            obj = form.save(commit=False)
            obj.save()
            event_detail = obj
            request.session['success_message_update'] = "Událost úspěšně aktualizována"

            return HttpResponseRedirect(reverse('kalendar:event', args=[event_detail.slug]))

    else:
        form = UpdateEventForm(instance=event_detail)

    form = UpdateEventForm(
        initial = {
            "title": event_detail.title,
            "event_type": event_detail.event_type,
            "event_date": event_detail.event_date,
            "termin_prihl": event_detail.termin_prihl,
            "bulletin": event_detail.bulletin,
            "zprava_info": event_detail.zprava_info,
            "zprava_warning": event_detail.zprava_warning,
            "start00": event_detail.start00,
            "gps": event_detail.gps,
            "discipline": event_detail.discipline,
            "contact": event_detail.contact,
            "pokyny": event_detail.pokyny,
            "startlist": event_detail.startlist,
            "splittimes": event_detail.splittimes,
            "results": event_detail.results,
            "mapa": event_detail.mapa,
        }
    )

    context['form'] = form
    context['event_detail'] = event_detail
    return render(request, 'kalendar/event_edit.html', context)

def event_entry_view(request, slug):
    event_detail = get_object_or_404(BlogPost, slug=slug)
    current_time = timezone.now()
    
    age = None
    sex = None
    initial_data = {}

    if event_detail.termin_prihl <= current_time:
        context = {'event_detail': event_detail, 'message': "Přihlašování uzavřeno"}
        return render(request, 'kalendar/entry_form.html', context)
    
    if request.method == 'POST':
        form = EventEntryForm(request.POST)
        if form.is_valid():
            si_number = form.cleaned_data['si_number']
            index = form.cleaned_data['index']

            if not (1000 <= si_number <= 8999999):
                form.add_error('si_number', "Neplatné číslo čipu")

            # Check for duplicate si_number within the form
            if EventEntry.objects.filter(event=event_detail, si_number=si_number).exists():
                form.add_error('si_number', "Toto číslo čipu je již v soutěži použito")

            # Check for duplicate index within the form
            if EventEntry.objects.filter(event=event_detail, index=index).exists():
                form.add_error('index', "Index je již v soutěži přihlášen")

            if not form.errors:
                form.instance.event = event_detail
                form.save()
                request.session['success_message_entry'] = "Úspěšně jste se přihlásili na tuto událost."
                return redirect('kalendar:event', slug=slug)  # Redirect to event detail page
    else:
        if request.user.is_authenticated:
            user = request.user
            initial_data = {
                'first_name': user.first_name,
                'second_name': user.second_name,
                'index': user.index,
                'si_number': user.si_number,
            }
            age = user.age 
            sex = user.sex  

        form = EventEntryForm(initial=initial_data)
    
    context = {
        'event_detail': event_detail,
        'form': form,
        'age': age,
        'sex': sex,
    }
    
    return render(request, 'kalendar/entry_form.html', context)




@login_required
def event_entry_edit_view(request, slug):
    event_detail = get_object_or_404(BlogPost, slug=slug)
    participants = EventEntry.objects.filter(event=event_detail)

    is_organizer = request.user.is_organizator
    
    current_time = timezone.now()
    if event_detail.termin_prihl <= current_time:
        request.session['success_message_entry_cantupdate'] = "Přihlašování je pro tuto událost uzavřeno"
        return redirect('kalendar:event', slug=slug)
    
    try:
        user_entry = EventEntry.objects.get(event=event_detail, index=request.user.index)
    except EventEntry.DoesNotExist:
        request.session['success_message_entry_cantupdate'] = "Nejsi v této události přihlášen, proto přihlášku nemůžeš upravit"
        return redirect('kalendar:event', slug=slug)
    
    if request.method == 'POST':
        form = EventEntryForm(request.POST, instance=user_entry)
        form.fields.pop('index', None)
        if 'delete_entry' in request.POST:
            user_entry.delete()
            request.session['success_message_entry_delete'] = "Přihláška úspěšně smazána"
            return redirect('kalendar:event', slug=slug)
        if form.is_valid():
            si_number = form.cleaned_data['si_number']
            
            user_account = Account.objects.get(index=request.user.index)
            age = user_account.age  
            sex = user_account.sex

            if sex == 'F':
                if age <= 12:
                    categories = ['mdr', 'd12', 'd14', 'd16', 'd19', 'd20']
                elif age <= 14:
                    categories = ['d14', 'd16', 'd19', 'd20']
                elif age <= 16:
                    categories = ['d16', 'd19', 'd20']
                elif age <= 19:
                    categories = ['d19', 'd20']
                elif age <= 34:
                    categories = ['d20']
                elif age <= 44:
                    categories = ['d35', 'd20']
                elif age <= 54:
                    categories = ['d45', 'd35', 'd20']
                elif age <= 64:
                    categories = ['d55', 'd45', 'd35', 'd20']
                elif age <= 99:
                    categories = ['d65', 'd55', 'd45', 'd35', 'd20']

            else:
                if age <= 12:
                    categories = ['mdr', 'm12', 'm14', 'm16', 'm19', 'm20']
                elif age <= 14:
                    categories = ['m14', 'm16', 'm19', 'm20']
                elif age <= 16:
                    categories = ['m16', 'm19', 'm20']
                elif age <= 19:
                    categories = ['m19', 'm20']
                elif age <= 39:
                    categories = ['m20']
                elif age <= 49:
                    categories = ['m40', 'm20']
                elif age <= 59:
                    categories = ['m50', 'm40', 'm20']
                elif age <= 69:
                    categories = ['m60', 'm50', 'm40', 'm20']
                elif age <= 99:
                    categories = ['m70', 'm60', 'm50', 'm40', 'm20']
                
                else:
                    categories = []

            existing_entry_si = EventEntry.objects.filter(event=event_detail, si_number=si_number).exclude(id=user_entry.id).first()
            if existing_entry_si:
                form.add_error('si_number', "Toto číslo čipu je již v soutěži použito")
                context = {
                    'event_detail': event_detail,
                    'form': form,
                    'participants': participants,
                    'is_organizer': is_organizer,
                    'categories': categories,
                }
                return render(request, 'kalendar/entry_edit.html', context)
            
            if si_number < 1000 or si_number > 8999999:
                form.add_error('si_number', "Neplatné číslo čipu")
                context = {
                    'event_detail': event_detail,
                    'form': form,
                    'participants': participants,
                    'is_organizer': is_organizer,
                    'categories': categories,
                }
                return render(request, 'kalendar/entry_edit.html', context)
            
            else:
                form.save()
                request.session['success_message_entry_update'] = "Přihláška úspěšně upravena"
                return redirect('kalendar:event', slug=slug)
    else:
        initial_category = user_entry.category
        form = EventEntryForm(instance=user_entry, initial={'category': initial_category})
        form.fields.pop('index', None)

        user_account = Account.objects.get(index=request.user.index)
        age = user_account.age  
        sex = user_account.sex

        if sex == 'F':
            if age <= 12:
                categories = ['mdr', 'd12', 'd14', 'd16', 'd19', 'd20']
            elif age <= 14:
                categories = ['d14', 'd16', 'd19', 'd20']
            elif age <= 16:
                categories = ['d16', 'd19', 'd20']
            elif age <= 19:
                categories = ['d19', 'd20']
            elif age <= 34:
                categories = ['d20']
            elif age <= 44:
                categories = ['d35', 'd20']
            elif age <= 54:
                categories = ['d45', 'd35', 'd20']
            elif age <= 64:
                categories = ['d55', 'd45', 'd35', 'd20']
            elif age <= 99:
                categories = ['d65', 'd55', 'd45', 'd35', 'd20']

        else:
            if age <= 12:
                categories = ['mdr', 'm12', 'm14', 'm16', 'm19', 'm20']
            elif age <= 14:
                categories = ['m14', 'm16', 'm19', 'm20']
            elif age <= 16:
                categories = ['m16', 'm19', 'm20']
            elif age <= 19:
                categories = ['m19', 'm20']
            elif age <= 39:
                categories = ['m20']
            elif age <= 49:
                categories = ['m40', 'm20']
            elif age <= 59:
                categories = ['m50', 'm40', 'm20']
            elif age <= 69:
                categories = ['m60', 'm50', 'm40', 'm20']
            elif age <= 99:
                categories = ['m70', 'm60', 'm50', 'm40', 'm20']
            
            else:
                categories = []

        print("Categories:", categories)
        context = {
            'event_detail': event_detail,
            'form': form,
            'participants': participants,
            'is_organizer': is_organizer,
            'categories': categories,
        }
        return render(request, 'kalendar/entry_edit.html', context)

@login_required
def event_entry_edit_all_view(request, slug):
    event_detail = get_object_or_404(BlogPost, slug=slug)
    
    if not organizator_same_club_only(request.user, event_detail):
        # Redirect or display an error message
        request.session['success_message_entries_cantupdate'] = "Nemáš oprávnění upravovat hromadně všechny přihlášky"
        return HttpResponseRedirect(reverse('kalendar:event', args=[event_detail.slug]))

    participants = EventEntry.objects.filter(event=event_detail)
    entry_forms = [EventEntryForm(instance=participant, prefix=f'participant_{participant.id}') for participant in participants]
    new_entry_form = EventEntryForm()  # Initialize new_entry_form for GET request

    if request.method == 'POST':
        if 'delete_entries' in request.POST:
            selected_entries = []
            for form in entry_forms:
                checkbox_name = f'delete_checkbox_{form.instance.id}'
                if checkbox_name in request.POST and request.POST[checkbox_name] == 'true':
                    selected_entries.append(form.instance)

            for entry in selected_entries:
                entry.delete()

            request.session['success_message_entries_delete'] = f"Bylo smázáno {len(selected_entries)} přihlášek."
            return redirect('kalendar:event', slug=event_detail.slug)
        
        elif 'edit_entries' in request.POST:
            updated_forms = []  # Store updated forms with potential errors
            
            for form in entry_forms:
                prefix = form.prefix
                form_instance = form.instance
                form_data = request.POST.copy()
                form_data.update({f'{prefix}-id': form_instance.id})
                updated_form = EventEntryForm(form_data, instance=form_instance, prefix=prefix)
                if updated_form.is_valid():
                    si_number = updated_form.cleaned_data['si_number']
                    index = updated_form.cleaned_data['index']

                    if not (1000 <= si_number <= 8999999):
                        updated_form.add_error('si_number', "Neplatné číslo čipu")

                    if EventEntry.objects.filter(event=event_detail, si_number=si_number).exclude(id=form_instance.id).exists():
                        updated_form.add_error('si_number', "Toto číslo čipu je již v soutěži použito")

                    if EventEntry.objects.filter(event=event_detail, index=index).exclude(id=form_instance.id).exists():
                        updated_form.add_error('index', "Index je již v soutěži přihlášen")

                    updated_forms.append(updated_form)  # Add the form to the list
            
            if all(form.is_valid() for form in updated_forms):
                for form in updated_forms:
                    form.save()
                request.session['success_message_entries_update'] = "Přihlášky byly úspěšně uloženy"
            else:
                # There are errors in the forms, stay on the same page and show errors
                context = {
                    'event_detail': event_detail,
                    'entry_forms': updated_forms,  # Use updated_forms with error messages
                    'new_entry_form': new_entry_form,
                }
                return render(request, 'kalendar/entry_edit_all.html', context)
            
            # Redirect to event_detail page after successful submission
            return redirect('kalendar:event', slug=event_detail.slug)

        elif 'add_new_entry' in request.POST:
            new_entry_form = EventEntryForm(request.POST)
            if new_entry_form.is_valid():
                si_number = new_entry_form.cleaned_data['si_number']
                index = new_entry_form.cleaned_data['index']

                if not (1000 <= si_number <= 8999999):
                    new_entry_form.add_error('si_number', "Neplatné číslo čipu")

                if EventEntry.objects.filter(event=event_detail, si_number=si_number).exists():
                    new_entry_form.add_error('si_number', "Toto číslo čipu je již v soutěži použito")

                if EventEntry.objects.filter(event=event_detail, index=index).exists():
                    new_entry_form.add_error('index', "Index je již v soutěži přihlášen")

                if not new_entry_form.errors:
                    new_entry = new_entry_form.save(commit=False)
                    new_entry.event = event_detail
                    new_entry.save()
                    new_entry_form = EventEntryForm()  # Reset the form after successful submission
                    request.session['success_message_new_from_entries'] = "Nová přihláška úspěšně přidána"
                    # Redirect to event_detail page after successful submission
                    return redirect('kalendar:event', slug=event_detail.slug)

    context = {
        'event_detail': event_detail,
        'entry_forms': entry_forms,
        'new_entry_form': new_entry_form,
    }

    return render(request, 'kalendar/entry_edit_all.html', context)







def event_participans_download_csv(request, slug):
    event_detail = get_object_or_404(BlogPost, slug=slug)
    participants = EventEntry.objects.filter(event=event_detail)

    response = HttpResponse(content_type='text/csv')
    filename = f"{slugify(event_detail.title)}_ucastnici.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Jméno', 'Příjmení', 'Index', 'Číslo čipu', 'Kategorie', 'Poznámka'])

    for participant in participants:
        writer.writerow([participant.first_name, participant.second_name, participant.index, participant.si_number, participant.get_category_display(), participant.note])

    return response


def event_participans_download_xlsx(request, slug):
    event_detail = get_object_or_404(BlogPost, slug=slug)
    participants = EventEntry.objects.filter(event=event_detail)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"{slugify(event_detail.title)}_ucastnici.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    wb = Workbook()
    ws = wb.active
    ws.title = 'Účastníci'
    ws.append(['Jméno', 'Příjmení', 'Index', 'Číslo čipu', 'Kategorie', 'Poznámka'])

    for participant in participants:
        ws.append([participant.first_name, participant.second_name, participant.index, participant.si_number, participant.get_category_display(), participant.note])

    wb.save(response)
    return response


