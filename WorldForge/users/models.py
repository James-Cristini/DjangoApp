# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from cStringIO import StringIO
from PIL import Image
import os


t1_caps = {
    'max_worlds': 1,
    'max_tiles_per_world': 10,
    'max_categories_per_world': 5,
    'max_things_per_world': 20,
}

t2_caps = {
    'max_worlds': 2,
    'max_tiles_per_world': 30,
    'max_categories_per_world': 15,
    'max_things_per_world': 50,
}

t3_caps = {
    'max_worlds': 4,
    'max_tiles_per_world': 100,
    'max_categories_per_world': 50,
    'max_things_per_world': 200,
}

t5_caps = {
    'max_worlds': 99999,
    'max_tiles_per_world': 99999,
    'max_categories_per_world': 99999,
    'max_things_per_world': 99999,
}

TIER_CAPS = {
 1: t1_caps,
 2: t2_caps,
 3: t3_caps,
 5: t5_caps,
}

PROFILE_THUMB_SIZE = (99, 66)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default_profile.jpg', upload_to='profile_pics')
    image_thumb = models.ImageField(default='default_profile_thumb.jpg', upload_to='profile_pics/thumbs')

    user_tier = models.IntegerField(default=1)

    def get_caps(self):
        return TIER_CAPS[self.user_tier]

    def __str__(self):
        return '{0} Profile'.format(self.user.username)

    def save(self, *args, **kwargs):
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

        self.create_thumbnail()

        force_update = False

        # If the instance already has been saved, it has an id and we set
        # force_update to True
        if self.id:
            force_update = True
        super(Profile, self).save(force_update=force_update, *args, **kwargs)

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
        image.thumbnail(PROFILE_THUMB_SIZE, Image.ANTIALIAS)

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