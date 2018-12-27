# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import World, Tile, Category, Thing

# Register your models here.
admin.site.register(World)
admin.site.register(Tile)
admin.site.register(Category)
admin.site.register(Thing)
