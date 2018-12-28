# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from .models import World, Category, Thing, Tile


def home(request):
    """ Home Page, log in, can eventually be news/etc. as well. """
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'forge/home.html', context)

def browse_worlds(request):
    """ """
    worlds = World.objects.filter(is_public=True).order_by('name')
    context = {'worlds': worlds}
    return render(request, 'forge/browse_worlds.html', context)

def world_index(request, username):
    """ List of ALL of the user's worlds """
    print username
    user_obj = User.objects.get(username=username)
    worlds = World.objects.filter(creator=user_obj)
    is_user = True if request.user == user_obj else False
    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'worlds': worlds
        }
    return render(request, 'forge/world_index.html', context)

def world_detail(request, username, world_name):
    """ Detail page for the given world, shows all Tiles with optional hide/show Categories/Thing list"""
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    tiles = Tile.objects.filter(creator=user_obj, world=world)
    categories = Category.objects.filter(creator=user_obj, world=world)
    things = Thing.objects.filter(creator=user_obj, world=world)
    is_user = True if request.user == user_obj else False

    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'world': world,
        'tiles': tiles,
        'categories':categories,
        'things': things,
        }
    return render(request, 'forge/world_detail.html', context)

def tile_detail(request, username, world_name, tile_name):
    """ Detail page for a specific Thing. """
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    print username, world_name, tile_name
    tile = Tile.objects.get(creator=user_obj, world=world, name=tile_name)
    categories = Category.objects.filter(creator=user_obj, world=world, tile=tile)
    things = Thing.objects.filter(creator=user_obj, world=world, tiles__in=[tile])
    is_user = True if request.user == user_obj else False
    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'world': world,
        'tile': tile,
        'categories': categories,
        'things': things,
        }
    return render(request, 'forge/tile_detail.html', context)

def category_index(request, username, world_name):
    """ Show just an index of ALL categories within the given world. """
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    categories = Category.objects.filter(creator=user_obj, world=world)
    things = Thing.objects.filter(creator=user_obj, world=world)
    is_user = True if request.user == user_obj else False
    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'world': world,
        'categories': categories,
        'things': things,
        }
    return render(request, 'forge/category_index.html', context)

def category_detail(request, username, world_name, category_name):
    """ Details a specific category, functions as an item index for that category as well. """
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    category = Category.objects.get(creator=user_obj, world=world, name=category_name)
    things = Thing.objects.filter(category=category)
    is_user = True if request.user == user_obj else False
    print 'WORLDNAME', world.name
    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'world': world,
        'category': category,
        'things': things,
        }
    return render(request, 'forge/category_detail.html', context)

def thing_detail(request, username, world_name, category_name, thing_name):
    """ Detail page for a specific Thing. """
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    category = Category.objects.get(creator=user_obj, world=world, name=category_name)
    thing = Thing.objects.get(creator=user_obj, world=world, name=thing_name)
    tiles = thing.tiles.all()
    is_user = True if request.user == user_obj else False
    context = {
        'is_user': is_user,
        'user_obj':user_obj,
        'world': world,
        'category': category,
        'thing': thing,
        'tiles': tiles,
        }
    return render(request, 'forge/thing_detail.html', context)


class WorldCreateView(LoginRequiredMixin, CreateView):
    """ Create a new world. Worlds can be created in the "world_index" page IF the session's user
        matches the world_index of the user. """

    model = World
    fields = ['name', 'genre', 'description', 'story', 'image', 'image_credit', 'is_public']
    template_name = 'forge/create_item.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        ### Currently able to create a new world through direct url containing a differnt user's username but still creates the world on the request.user's page
        # e.g. user jacristi can go to forge/newuser1/create_new_world/ and create a new world, but the world is created on jacristi's page/profile
        return super(WorldCreateView, self).form_valid(form)

class WorldUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """ Update a world, a world can only be updated by the world's creator. """

    model = World
    fields = ['name', 'genre', 'description', 'story', 'image', 'image_credit', 'is_public']
    template_name = 'forge/update_item.html'

    def form_valid(self, form):
        return super(WorldUpdateView, self).form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.creator:
            return True
        else:
            return False

class WorldDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """ Delete a world, removes all contained Tiles/Categories/Things.
        Worlds can only be deleted from the user's Profile page. """

    model = World
    success_url = 'forge_home' # Changes to world_index if UserPassesTestMixin

    def test_func(self):
        obj = self.get_object()
        context = {'username': self.kwargs.get('username')}
        if self.request.user == obj.creator:
            self.success_url = reverse('profile')
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False


class TileCreateView(LoginRequiredMixin, CreateView):
    model = Tile
    fields = ['name', 'description', 'story', 'image', 'image_credit']
    template_name = 'forge/create_item.html'

    def form_valid(self, form):
        user_obj = User.objects.get(username=self.kwargs['username'])
        if self.request.user != user_obj: # Check that the current user matches the creator of world being edited
            messages.error(self.request, 'You do not have permission to edit that world.')
            return redirect('forge_home')
        world = World.objects.get(creator=user_obj, name=self.kwargs['world_name'])
        form.instance.creator = self.request.user
        form.instance.world = world
        return super(TileCreateView, self).form_valid(form)


class TileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Tile
    fields = ['name', 'description', 'story', 'image', 'image_credit']
    template_name = 'forge/update_item.html'

    def form_valid(self, form):
        return super(TileUpdateView, self).form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.creator:
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False

class TileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Tile
    success_url = 'forge_home' # Changes to world_detail if UserPassesTestMixin

    def test_func(self):
        obj = self.get_object()
        context = {
            'username': self.kwargs.get('username'),
            'world_name': self.kwargs.get('world_name')
            }
        if self.request.user == obj.creator:
            self.success_url = reverse('world_detail', kwargs=context)
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    template_name = 'forge/create_item.html'

    def form_valid(self, form):
        x = self.get_context_data()
        print x
        user_obj = User.objects.get(username=self.kwargs['username'])
        if self.request.user != user_obj: # Check that the current user matches the creator of world being edited
            messages.error(self.request, 'You do not have permission to edit that world.')
            return redirect('forge_home')
        world = World.objects.get(creator=user_obj, name=self.kwargs['world_name'])
        tile_src = self.kwargs.get('tile_name')
        form.instance.created_tile_name = tile_src
        tile_obj = None

        # Add tile to the Thing's M2M tiles field if it was created at a tile_detail page
        if tile_src not in ['created_from_world', 'created_from_category_index', 'created_from_category_detail']:
            tile_obj = Tile.objects.get(creator=user_obj, world=world, name=tile_src)
            form.instance.created_tile_name = tile_obj.name

        form.instance.creator = self.request.user
        form.instance.world = world
        super(CategoryCreateView, self).form_valid(form)
        if tile_obj:
            form.instance.tile.add(tile_obj)

        return redirect(form.instance.get_absolute_url())

class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = ['name', 'description'] # tile
    template_name = 'forge/update_item.html'

    def form_valid(self, form):
        form.instance.created_tile_name = 'updated_from_category_page'
        return super(CategoryUpdateView, self).form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.creator:
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False

class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    success_url = 'forge_home'

    def test_func(self):
        obj = self.get_object()
        context = {
            'username': self.kwargs.get('username'),
            'world_name': self.kwargs.get('world_name')
        }
        if self.request.user == obj.creator:
            self.success_url = reverse('world_detail', kwargs=context)
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False


class ThingCreateView(LoginRequiredMixin, CreateView):
    model = Thing
    fields = ['name', 'description', 'story', 'image', 'image_credit']
    template_name = 'forge/create_item.html'

    def form_valid(self, form):
        user_obj = User.objects.get(username=self.kwargs['username'])
        if self.request.user != user_obj: # Check that the current user matches the creator of world being edited
            messages.error(self.request, 'You do not have permission to edit that world.')
            return redirect('forge_home')
        world = World.objects.get(creator=user_obj, name=self.kwargs['world_name'])
        #tile_obj = Tile.objects.get(creator=user_obj, world=world, name=self.kwargs.get('tile_name'))
        category = Category.objects.get(creator=user_obj, world=world, name=self.kwargs.get('category_name'))
        tile_src = self.kwargs.get('tile_name')
        form.instance.created_tile_name = tile_src
        tile_obj = None

        # Add tile to the Thing's M2M tiles field if it was created at a tile_detail page
        if tile_src not in ['created_from_world', 'created_from_category_index', 'created_from_category_detail']:
            tile_obj = Tile.objects.get(creator=user_obj, world=world, name=tile_src)
            form.instance.created_tile_name = tile_obj.name

        form.instance.creator = self.request.user
        form.instance.world = world
        form.instance.category = category
        super(ThingCreateView, self).form_valid(form)
        if tile_obj:
            form.instance.tiles.add(tile_obj)

        return redirect(form.instance.get_absolute_url())

class ThingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Thing
    fields = ['name', 'description', 'story', 'image', 'image_credit']
    template_name = 'forge/update_item.html'

    def form_valid(self, form):
        form.instance.created_tile_name = 'updated_from_thing_page'
        return super(ThingUpdateView, self).form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.creator:
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False

class ThingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Thing
    success_url = 'forge_home'

    def test_func(self):
        obj = self.get_object()
        context = {
            'username': self.kwargs.get('username'),
            'world_name': self.kwargs.get('world_name'),
            'category_name':self.kwargs.get('category_name')
        }
        if self.request.user == obj.creator:
            self.success_url = reverse('category_detail', kwargs=context)
            return True
        else:
            messages.error(self.request, 'You do not have permission to edit that.')
            return False

### TODO make so world's can only be DELETED on the user's profile page
### TODO create a Tile table on world_detail pages, saves location of item in table
### TODO option to start with a "templated" world? (start with a few categories started)