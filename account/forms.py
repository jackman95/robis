from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from datetime import date

from account.models import Account



class RegistrationForm(UserCreationForm):
        email = forms.EmailField(max_length=60, help_text="Vyžadováno, zadejte platný email")
        
        class Meta:
                model = Account
                fields = ('username', 'email', 'password1', 'password2', 'first_name', 'second_name', 'index', 'si_number')

class AccountAuthenticationForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, initial=False, widget=forms.CheckboxInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['remember_me'].label = "Zapamatuj si mě"
    
class AccountAuthenticationForm(forms.ModelForm):

        password = forms.CharField(label='Password', widget=forms.PasswordInput)

        class Meta:
                model = Account
                fields = ('username', 'password')

        def clean(self):
                if self.is_valid ():
                        username = self.cleaned_data['username']
                        password = self.cleaned_data['password']
                        if not authenticate(username=username, password=password):
                                raise forms.ValidationError("Nesprávný údaj")  
                        
class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'second_name', 'index', 'si_number')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" je již obsazen' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            username = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Uživatelské jméno "%s" je již obsazeno' % username)

    def clean_index(self):
        index = self.cleaned_data['index']
        try:
            index = Account.objects.exclude(pk=self.instance.pk).get(index=index)
        except Account.DoesNotExist:
            return index
        raise forms.ValidationError('Index "%s" je již obsazen' % index)

    def clean_si_number(self):
        si_number = self.cleaned_data['si_number']
        try:
            si_number = Account.objects.exclude(pk=self.instance.pk).get(si_number=si_number)
        except Account.DoesNotExist:
            return si_number
        raise forms.ValidationError('Číslo čipu "%s" je již obsazeno' % si_number)
    

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Update the club, age, and sex fields based on the new index
        instance.club = instance.index[:3].upper()

        birth_year = int(instance.index[3:5])
        current_year = date.today().year % 100

        if 0 <= birth_year <= current_year:
            instance.age = current_year - birth_year
        else:
            instance.age = (100 - birth_year + current_year) % 100

        sex_code = int(instance.index[5:7])
        instance.sex = 'F' if sex_code >= 50 else 'M'
        
        if commit:
            instance.save()
        return instance
    
    
     