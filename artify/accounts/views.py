from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from artify.accounts.forms import SignUpForm, SignInForm, ProfileForm
from artify.accounts.models import Profile
from artify.art_items.models import ArtItem


def sign_in_user(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list items')
    else:
        form = SignInForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signin.html', context)


def sign_up_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list items')
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


@login_required
def sign_out_user(request):
    logout(request)
    return redirect('landing page')


@login_required
def profile_details(request):
    profile = Profile.objects.get(pk=request.user.id)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile details')
    else:
        form = ProfileForm(instance=profile)

    user_items = ArtItem.objects.filter(user_id=request.user.id)

    context = {
        'form': form,
        'art_items': user_items,
        'profile': profile,
    }
    return render(request, 'accounts/user_profile.html', context)
