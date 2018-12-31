# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from forge.models import World, Tile, Category, Thing
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


def register(request):
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created')

            ### Automatically log in user after registering
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)

            if user is not None:
                login(request, user)
                profile = Profile(user=user)
                profile.save()
                return redirect('forge_home')

            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
    """
    context = {}
    return render(request, 'users/temp_register.html', context)

@login_required
def profile(request):
    user = request.user
    profile = request.user.profile
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    caps = profile.get_caps()
    max_worlds = caps['max_worlds']
    max_tiles = caps['max_tiles_per_world']
    max_categories = caps['max_categories_per_world']
    max_things = caps['max_things_per_world']

    user_worlds = World.objects.filter(creator=user)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'user_worlds': user_worlds,
        'max_worlds': max_worlds,
        'max_tiles': max_tiles,
        'max_categories': max_categories,
        'max_things': max_things,
    }
    return render(request, 'users/profile.html', context)