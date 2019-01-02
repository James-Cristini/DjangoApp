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
from users.models import Profile
from .tile_logic import get_matrix

def test_page(request):
    context = {}
    return render(request, 'forge/test.html', context)

def test_func(request, val):
    print 'VALUE', val
    return redirect('test_page')

def home(request):
    """ Home Page, log in, can eventually be news/etc. as well. """
    users = User.objects.all()
    profiles = Profile.objects.all()

    context = {
        'users': users,
        'profiles': profiles,
        'home_active': 'active',
    }

    return render(request, 'forge/home.html', context)

def browse_worlds(request):
    """ """
    users = User.objects.all()
    worlds = World.objects.filter(is_public=True).order_by('name')

    context = {
        'users': users,
        'worlds': worlds,
        'browse_active': 'active',
        }

    return render(request, 'forge/browse_worlds.html', context)

def world_index(request, username):
    """ List of ALL of the user's worlds """
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    worlds = World.objects.filter(creator=user_obj)
    can_edit = True if request.user == user_obj else False
    can_add_world = False

    if request.user == user_obj:
        user_active = 'active'
        user_obj_active = None
        can_edit = True
        caps = profile.get_caps()

        if len(worlds) < caps['max_worlds']:
            can_add_world = True
    else:
        user_active = None
        user_obj_active = 'active'

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_world': can_add_world,
        'user_obj':user_obj,
        'worlds': worlds,
        'user_active': user_active,
        'user_obj_active': user_obj_active,
        }

    return render(request, 'forge/world_index.html', context)

def world_detail(request, username, world_name):
    """ Detail page for the given world, shows all Tiles with optional hide/show Categories/Thing list"""
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    world = World.objects.get(creator=user_obj, name=world_name)
    tiles = Tile.objects.filter(creator=user_obj, world=world).order_by('pk')
    categories = Category.objects.filter(creator=user_obj, world=world).order_by('pk')
    things = Thing.objects.filter(creator=user_obj, world=world).order_by('pk')

    can_edit = False
    can_add_tile = False
    can_add_category = False
    can_add_thing = False

    if request.user == user_obj:
        can_edit = True
        caps = profile.get_caps()

        if len(tiles) < caps['max_tiles_per_world']:
            can_add_tile = True

        if len(categories) < caps['max_categories_per_world']:
            can_add_category = True

        if len(things) < caps['max_things_per_world']:
            can_add_thing = True

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_tile': can_add_tile,
        'can_add_category': can_add_category,
        'can_add_thing': can_add_thing,
        'user_obj':user_obj,
        'world': world,
        'tiles': tiles,
        'categories':categories,
        'things': things,
        'world_active': 'active',
        }

    return render(request, 'forge/world_detail.html', context)

def tile_index(request, username, world_name):
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    world = World.objects.get(creator=user_obj, name=world_name)
    tiles = Tile.objects.filter(creator=user_obj, world=world)

    tile_matrix = get_matrix(tiles)

    can_edit = False
    can_add_tile = False

    if request.user == user_obj:
        can_edit = True
        caps = profile.get_caps()

        if len(tiles) < caps['max_tiles_per_world']:
            can_add_tile = True

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_tile': can_add_tile,
        'user_obj':user_obj,
        'world': world,
        'tiles': tiles,
        'tile_matrix': tile_matrix,
        'tiles_active': 'active',
        }

    return render(request, 'forge/tile_index.html', context)

def tile_detail(request, username, world_name, tile_name):
    """ Detail page for a specific Thing. """
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    world = World.objects.get(creator=user_obj, name=world_name)
    tile = Tile.objects.get(creator=user_obj, world=world, name=tile_name)
    categories = Category.objects.filter(creator=user_obj, world=world).order_by('pk')
    things = Thing.objects.filter(creator=user_obj, world=world, tiles__in=[tile]).order_by('pk')
    all_things = Thing.objects.filter(creator=user_obj, world=world).order_by('pk')
    can_edit = False
    can_add_category = False
    can_add_thing = False

    if request.user == user_obj:
        can_edit = True
        caps = profile.get_caps()

        if len(categories) < caps['max_categories_per_world']:
            can_add_category = True

        if len(all_things) < caps['max_things_per_world']:
            can_add_thing = True

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_category': can_add_category,
        'can_add_thing': can_add_thing,
        'user_obj':user_obj,
        'world': world,
        'tile': tile,
        'categories': categories,
        'things': things,
        }

    return render(request, 'forge/tile_detail.html', context)

def category_index(request, username, world_name):
    """ Show just an index of ALL categories within the given world. """
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    world = World.objects.get(creator=user_obj, name=world_name)
    categories = Category.objects.filter(creator=user_obj, world=world).order_by('pk')
    things = Thing.objects.filter(creator=user_obj, world=world).order_by('pk')
    can_edit = False
    can_add_category = False
    can_add_thing = False

    if request.user == user_obj:
        can_edit = True
        caps = profile.get_caps()

        if len(categories) < caps['max_categories_per_world']:
            can_add_category = True

        if len(things) < caps['max_things_per_world']:
            can_add_thing = True

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_category': can_add_category,
        'can_add_thing': can_add_thing,
        'user_obj':user_obj,
        'world': world,
        'categories': categories,
        'things': things,
        'categories_active': 'active',
        }

    return render(request, 'forge/category_index.html', context)

def category_detail(request, username, world_name, category_name):
    """ Details a specific category, functions as an item index for that category as well. """
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    world = World.objects.get(creator=user_obj, name=world_name)
    category = Category.objects.get(creator=user_obj, world=world, name=category_name)
    things = Thing.objects.filter(creator=user_obj, world=world,category=category).order_by('pk')
    all_things = Thing.objects.filter(creator=user_obj, world=world).order_by('pk')
    can_edit = False
    can_add_thing = False

    if request.user == user_obj:
        can_edit = True
        caps = profile.get_caps()

        if len(all_things) < caps['max_things_per_world']:
            can_add_thing = True

    context = {
        'users': users,
        'can_edit': can_edit,
        'can_add_thing': can_add_thing,
        'user_obj':user_obj,
        'world': world,
        'categories': [category],
        'things': things,
        }

    return render(request, 'forge/category_detail.html', context)

def thing_detail(request, username, world_name, category_name, thing_name):
    """ Detail page for a specific Thing. """
    users = User.objects.all()
    user_obj = User.objects.get(username=username)
    world = World.objects.get(creator=user_obj, name=world_name)
    category = Category.objects.get(creator=user_obj, world=world, name=category_name)
    thing = Thing.objects.get(creator=user_obj, world=world, category=category, name=thing_name)
    tiles = thing.tiles.all()
    can_edit = True if request.user == user_obj else False
    context = {
        'users': users,
        'can_edit': can_edit,
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
        user = self.request.user
        form.instance.creator = user
        ### Currently able to create a new world through direct url containing a differnt user's username but still creates the world on the request.user's page
        # e.g. user jacristi can go to forge/newuser1/create_new_world/ and create a new world, but the world is created on jacristi's page/profile

        profile = Profile.objects.get(user=user)
        user_worlds = World.objects.filter(creator=user)

        caps = profile.get_caps()
        if len(user_worlds) >= caps['max_worlds']:
            messages.error(self.request, 'You cannot create any more Worlds.')
            return redirect('forge_home')

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
        user = self.request.user
        user_obj = User.objects.get(username=self.kwargs['username'])
        if user != user_obj: # Check that the current user matches the creator of world being edited
            messages.error(self.request, 'You do not have permission to edit that world.')
            return redirect('forge_home')
        world = World.objects.get(creator=user_obj, name=self.kwargs['world_name'])
        form.instance.creator = user
        form.instance.world = world

        form.instance.horizontal_position = int(self.kwargs.get('h_pos'))
        form.instance.vertical_position = int(self.kwargs.get('v_pos'))

        profile = Profile.objects.get(user=user)
        user_tiles = Tile.objects.filter(creator=user, world=world)

        caps = profile.get_caps()
        if len(user_tiles) >= caps['max_tiles_per_world']:
            messages.error(self.request, 'You cannot create any more Tiles.')
            return redirect('forge_home')

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
        user = self.request.user
        user_obj = User.objects.get(username=self.kwargs['username'])
        if user != user_obj: # Check that the current user matches the creator of world being edited
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

        form.instance.creator = user
        form.instance.world = world

        profile = Profile.objects.get(user=user)
        user_categories = Category.objects.filter(creator=user, world=world)

        caps = profile.get_caps()
        if len(user_categories) >= caps['max_categories_per_world']:
            messages.error(self.request, 'You cannot create any more Categories.')
            return redirect('forge_home')

        super(CategoryCreateView, self).form_valid(form)

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
        user = self.request.user
        user_obj = User.objects.get(username=self.kwargs['username'])
        if user != user_obj: # Check that the current user matches the creator of world being edited
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

        form.instance.creator = user
        form.instance.world = world
        form.instance.category = category

        profile = Profile.objects.get(user=user)
        user_things = Thing.objects.filter(creator=user, world=world)

        caps = profile.get_caps()
        if len(user_things) >= caps['max_things_per_world']:
            messages.error(self.request, 'You cannot create any more Things.')
            return redirect('forge_home')

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

"""
Pages:
--------
Home
User Profile
User Worlds
Browse Worlds
World Detail
Tile Index
Tile Detail
Category Index
Category Detail
Thing Detail
About Page
"""

### TODO double check all edit/add items are disabled properly when cap is reached
### TODO keep sub_nav affixed on horizontal scroll (especially on tile index page)
### TODO Able to add existing Things to multiple tiles without leaving the page (click a button in each category to see list of existing things to add?)
### TODO Merge Detail and Update views so the user can view AND change a World/Tile/Category/Thing on the same page

### TODO prettify pages, especially tile_index
### TODO option to start with a "templated" world? (start with a few categories already in place)
### TODO Prettify code :/

"""
### TODO collapse-able sections for Tiles/Categories on detail pages XXX Started

### Delete category option?
#       - Added delete category option back

--------
Done: 1/1/19
--------
### make default image in static
#       - serving static images when image/image_thumb is null (models now have imagefield -> blank=true)
### remove Tile M2M from Categories, all categories should be listed for each tile
#       - M2M field removed, kept some logic for proper redirects
"""