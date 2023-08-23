from django import forms

from kalendar.models import BlogPost, EventEntry, MicroEvent, MicroEventEntry

class CreateEventForm(forms.ModelForm):

    class Meta:
        model = BlogPost
        fields = ['title', 'event_type', 'event_date', 'termin_prihl', 'bulletin']

class UpdateEventForm(forms.ModelForm):

    delete_bulletin = forms.BooleanField(required=False, initial=False)
    delete_pokyny = forms.BooleanField(required=False, initial=False)
    delete_startlist = forms.BooleanField(required=False, initial=False)
    delete_results = forms.BooleanField(required=False, initial=False)
    delete_splittimes = forms.BooleanField(required=False, initial=False)
    delete_mapa = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'event_type', 'event_date', 'termin_prihl', 'zprava_info', 'zprava_warning', 'start00', 'discipline', 'gps', 'contact', 'mapa', 'bulletin', 'pokyny', 'startlist', 'results', 'splittimes']
       
    def save(self, commit=True):
        event_detail = super().save(commit=False)
        event_detail.title = self.cleaned_data['title']
        event_detail.event_type = self.cleaned_data['event_type']
        event_detail.event_date = self.cleaned_data['event_date']
        event_detail.termin_prihl = self.cleaned_data['termin_prihl']
        event_detail.zprava_info = self.cleaned_data['zprava_info']
        event_detail.zprava_warning = self.cleaned_data['zprava_warning']
        event_detail.start00 = self.cleaned_data['start00']
        event_detail.discipline = self.cleaned_data['discipline']
        event_detail.gps = self.cleaned_data['gps']
        event_detail.contact = self.cleaned_data['contact']



        if commit:
            event_detail.save()  # Save the event first to avoid "I/O operation on closed file" error

        # Set new files if available
        if self.cleaned_data['mapa']:
            event_detail.mapa = self.cleaned_data['mapa']
        if self.cleaned_data['bulletin']:
            event_detail.bulletin = self.cleaned_data['bulletin']
        if self.cleaned_data['pokyny']:
            event_detail.pokyny = self.cleaned_data['pokyny']
        if self.cleaned_data['startlist']:
            event_detail.startlist = self.cleaned_data['startlist']
        if self.cleaned_data['results']:
            event_detail.results = self.cleaned_data['results']
        if self.cleaned_data['splittimes']:
            event_detail.splittimes = self.cleaned_data['splittimes']


        # Check and delete files if corresponding delete fields are checked
        if self.cleaned_data['delete_bulletin']:
            event_detail.bulletin.delete()
        if self.cleaned_data['delete_pokyny']:
            event_detail.pokyny.delete()
        if self.cleaned_data['delete_startlist']:
            event_detail.startlist.delete()
        if self.cleaned_data['delete_results']:
            event_detail.results.delete()
        if self.cleaned_data['delete_splittimes']:
            event_detail.splittimes.delete()
        if self.cleaned_data['delete_mapa']:
            event_detail.mapa.delete()

        if commit:
            event_detail.save()
        
        return event_detail
    
class EventEntryForm(forms.ModelForm):
    class Meta:
        model = EventEntry
        fields = ['first_name', 'second_name', 'index', 'si_number', 'category', 'note']
        labels = {
            'first_name': 'Jméno',
            'second_name': 'Příjmení',
            'si_number': 'Číslo čipu',
            'category': 'Kategorie',
            'note': 'Poznámka',

        }

    def __init__(self, *args, **kwargs):
        super(EventEntryForm, self).__init__(*args, **kwargs)
        # You can customize the form if needed
        # For example, to exclude fields that you don't want to display
        # self.fields.pop('some_field_name')


class CreateMicroEventForm(forms.ModelForm):
    max_entries = forms.IntegerField(label='Míst', min_value=1, required=True)
    class Meta:
        model = MicroEvent
        fields = ['notice', 'max_entries']
        labels = {
            'notice': 'Odjezd',
            'max_entries': 'Míst',
        }

class MicroEventEntryForm(forms.ModelForm):
    class Meta:
        model = MicroEventEntry
        fields = ['name', 'notice_name']  # Use the correct field name
        labels = {
            'name': 'Jméno',
            'notice_name': 'Poznámka',
        }

    def __init__(self, *args, micro_event=None, **kwargs):
        super().__init__(*args, **kwargs)
        if micro_event:
            self.fields['microevent'].widget = forms.HiddenInput()
            self.fields['microevent'].initial = micro_event.id