from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from kalendar.views import EventEntry
from datetime import date


def registration_view(request):
    context = {}

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # Check if the index is valid (adjust the condition according to your validation)
            if len(user.index) != 7:
                form.add_error('index', "Index musí mít přesně 7 symbolů.")
                context['registration_form'] = form
                return render(request, 'account/register.html', context)

            # Set the 'club', 'age', and 'sex' fields based on 'index'
            user.club = user.index[:3].upper()

            birth_year = int(user.index[3:5])
            current_year = date.today().year % 100
            age = current_year - birth_year

            if 0 <= birth_year <= current_year:
                user.age = age
            else:
                user.age = (100 - birth_year + current_year) % 100

            sex_code = int(user.index[5:7])
            user.sex = 'F' if sex_code >= 50 else 'M'

            user.save()

            # Log the user in
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(username=username, password=raw_password)
            login(request, account)

            return redirect('home')
        else:
            context['registration_form'] = form
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)

        


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            remember_me = form.cleaned_data.get('remember_me')
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user,)
                if remember_me:
                    request.session.set_expiry(500)  # Set session expiry to 7 days (in seconds)
                else:
                    request.session.set_expiry(0)  # Set session expiry to browser session
		    	#Check if there is a next parameter in the URL
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)	
					
                return redirect('home')
    
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)

def account_view(request):

	if not request.user.is_authenticated:
		return redirect("login")

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
				"first_name": request.POST['first_name'],
				"second_name": request.POST['second_name'],
				"index": request.POST['index'],
				"si_number": request.POST['si_number'],
                "club": request.user.club,
                "age": request.user.age,
                "sex": request.user.sex,
			}
			form.save()
			context['success_message_acc_update'] = "Úspěšně aktualizováno!"
	else:
		form = AccountUpdateForm(
				initial= {
					"email": request.user.email,
					"username": request.user.username,
                    "first_name": request.user.first_name,
                    "second_name": request.user.second_name,
                    "index": request.user.index,
		    		"si_number": request.user.si_number,
					"club": request.user.club,
					"age": request.user.age,
					"sex": request.user.sex,
		                           
				}
			)
	context['account_form'] = form
	return render(request, 'account/account.html', context)

def must_authenticate_view(request):
	return render (request, 'account/must_authenticate.html', {})

def account_event_view(request):
    user = request.user
    user_entries = EventEntry.objects.filter(index=user.index).order_by('-event__event_date')
    today = date.today()
    context = {
        'user_entries': user_entries,
        'today': today,
    }

    return render(request, 'account/account_event.html', context)