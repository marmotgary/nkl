from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from kyykka.forms import SignUpForm

#
# def signup(request):
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             return redirect('complete')
#     else:
#         form = SignUpForm()
#     return render(request, 'signup.html', {'form': form})
from kyykka.models import Player


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('username')
            user.save()
            # user.refresh_from_db()
            Player.objects.create(user=user, number=form.cleaned_data.get('player_number'))
            return redirect('complete')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def success(request):
    return render(request, 'signup_complete.html')
