# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import models
from django.urls import reverse
from cStringIO import StringIO
from PIL import Image
import os

THUMBNAIL_SIZE = (99, 66)
WORLD_THUMB_SIZE = (250, 250)

def validate_name(name):
    if '\\' in name or '/' in name:
        raise ValidationError('Names cannot contain slashes.')


class World(models.Model):
    is_public = models.BooleanField(default=False)
    name = models.CharField(max_length=100, validators=[validate_name,])
    genre = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_world.jpg', upload_to='world_images')
    image_thumb = models.ImageField(default='default_world_thumb.jpg', upload_to='world_images/thumbs')
    image_credit = models.CharField(max_length=120, blank=True)
    str_name = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('str_name',)
        unique_together= (('creator', 'name'),)

    def __str__(self):
        return '{0} -- {1}'.format(self.creator.username, self.name)

    def save(self, *args, **kwargs):
        self.str_name = '{0} -- {1}'.format(self.creator.username, self.name)
        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set 
        # force_update to True
        if self.id:
            force_update = True
        super(World, self).save(force_update=force_update, *args, **kwargs)

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        if thumb_extension in ['.jpg', '.jpeg']:
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
            DJANGO_TYPE = 'image/jpeg'
        elif thumb_extension == '.gif':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'gif'
            DJANGO_TYPE = 'image/gif'
        elif thumb_extension == '.png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(WORLD_THUMB_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.image_thumb.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def get_absolute_url(self):
        return reverse('world_index', kwargs={'username':self.creator})

class Tile(models.Model):
    loc = None # Will be used for determining the location of Tiles in the grid/table on the page itself
    name = models.CharField(max_length=100, validators=[validate_name,])
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_tile.jpg', upload_to='tile_images')
    image_thumb = models.ImageField(default='default_tile_thumb.jpg', upload_to='tile_images/thumbs')
    image_credit = models.CharField(max_length=120, blank=True)
    str_name = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('str_name',)
        unique_together= (('creator', 'world', 'name'),)

    def __str__(self):
        return '{0} -- {1}'.format(self.world.name, self.name)

    def save(self, *args, **kwargs):
        self.str_name = '{0} -- {1}'.format(self.world.name, self.name)
        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True
        super(Tile, self).save(force_update=force_update, *args, **kwargs)

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        from PIL import Image
        from cStringIO import StringIO
        from django.core.files.uploadedfile import SimpleUploadedFile
        import os

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        if thumb_extension in ['.jpg', '.jpeg']:
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
            DJANGO_TYPE = 'image/jpeg'
        elif thumb_extension == '.gif':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'gif'
            DJANGO_TYPE = 'image/gif'
        elif thumb_extension == '.png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'

        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.image_thumb.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )

    def get_absolute_url(self):
        return reverse('world_detail', kwargs={'username':self.creator, 'world_name':self.world.name})


class Category(models.Model): # Tile will be the initial, default Category of Things
    name = models.CharField(max_length=100, validators=[validate_name,])
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    tile = models.ManyToManyField(Tile, blank=True) #Named incorrectly should be plural tiles, not singular tile
    created_tile_name = None
    str_name = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('str_name',)
        verbose_name_plural = "categories"
        unique_together= (('creator', 'world', 'name'),)

    def __str__(self):
        return '{0} -- {1}'.format(self.world.name, self.name)

    def get_absolute_url(self):
        if self.created_tile_name == 'created_from_world':
            return reverse('world_detail', kwargs={'username':self.creator, 'world_name':self.world.name})
        elif self.created_tile_name == 'created_from_category_index':
            return reverse('category_index', kwargs={'username':self.creator, 'world_name':self.world.name})
        elif self.created_tile_name == 'updated_from_category_page':
            return reverse('category_detail', kwargs={'username':self.creator, 'world_name':self.world.name, 'category_name':self.name})
        else:
            return reverse('tile_detail', kwargs={'username':self.creator, 'world_name':self.world.name, 'tile_name':self.created_tile_name})


    def save(self, *args, **kwargs):
        self.str_name = '{0} -- {1}'.format(self.world.name, self.name)
        super(Category, self).save(*args, **kwargs)


class Thing(models.Model):
    name = models.CharField(max_length=100, validators=[validate_name,])
    description = models.TextField(blank=True)
    story = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False)
    world = models.ForeignKey(World, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_thing.jpg', upload_to='thing_images')
    image_thumb = models.ImageField(default='default_thing_thumb.jpg', upload_to='thing_images/thumbs')
    image_credit = models.CharField(max_length=120, blank=True)
    tiles = models.ManyToManyField(Tile, blank=True)
    created_tile_name = None
    str_name = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ('str_name',)
        unique_together= (('creator', 'world', 'name', 'category'),)

    def __str__(self):
        return '{0} -- {1}'.format(self.world.name, self.name)

    def get_absolute_url(self):
        if self.created_tile_name == 'created_from_world':
            return reverse('world_detail', kwargs={'username':self.creator, 'world_name':self.world.name})
        elif self.created_tile_name == 'created_from_category_index':
            return reverse('category_index', kwargs={'username':self.creator, 'world_name':self.world.name})
        elif self.created_tile_name == 'created_from_category_detail':
            return reverse('category_detail', kwargs={'username':self.creator, 'world_name':self.world.name, 'category_name':self.category.name})
        elif self.created_tile_name == 'updated_from_thing_page':
            return reverse('thing_detail', kwargs={'username':self.creator, 'world_name':self.world.name, 'category_name':self.category.name, 'thing_name':self.name})
        else:
            return reverse('tile_detail', kwargs={'username':self.creator, 'world_name':self.world.name, 'tile_name':self.created_tile_name})

    def save(self, *args, **kwargs):
        self.str_name = '{0} -- {1}'.format(self.world.name, self.name)
        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True
        super(Thing, self).save(force_update=force_update, *args, **kwargs)

    def create_thumbnail(self):
        # original code for this method came from
        # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

        # If there is no image associated with this.
        # do not create thumbnail
        if not self.image:
            return

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        if thumb_extension in ['.jpg', '.jpeg']:
            PIL_TYPE = 'jpeg'
            FILE_EXTENSION = 'jpg'
            DJANGO_TYPE = 'image/jpeg'
        elif thumb_extension == '.gif':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'gif'
            DJANGO_TYPE = 'image/gif'
        elif thumb_extension == '.png':
            PIL_TYPE = 'png'
            FILE_EXTENSION = 'png'
            DJANGO_TYPE = 'image/png'


        # Open original photo which we want to thumbnail using PIL's Image
        image = Image.open(StringIO(self.image.read()))

        # We use our PIL Image object to create the thumbnail, which already
        # has a thumbnail() convenience method that contrains proportions.
        # Additionally, we use Image.ANTIALIAS to make the image look better.
        # Without antialiasing the image pattern artifacts may result.
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)

        # Save the thumbnail
        temp_handle = StringIO()
        image.save(temp_handle, PIL_TYPE)
        temp_handle.seek(0)

        # Save image to a SimpleUploadedFile which can be saved into
        # ImageField
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type=DJANGO_TYPE)
        # Save SimpleUploadedFile into image field
        self.image_thumb.save(
            '%s_thumbnail.%s' % (os.path.splitext(suf.name)[0], FILE_EXTENSION),
            suf,
            save=False
        )
