from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create_world/(?P<username>[A-Za-z0-9]+)/$', views.WorldCreateView.as_view(), name='create_world'),
    url(r'^update_world/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/$', views.WorldUpdateView.as_view(), name='update_world'),
    url(r'^delete_world/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/$', views.WorldDeleteView.as_view(), {'template_name': 'item_confirm_delete.html'}, name='delete_world',),
    url(r'^create_tile/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/$', views.TileCreateView.as_view(), name='create_tile'),
    url(r'^update_tile/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<tile_name>[^\\]+)/$', views.TileUpdateView.as_view(), name='update_tile'),
    url(r'^delete_tile/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<tile_name>[^\\]+)/$', views.TileDeleteView.as_view(), name='delete_tile'),
    url(r'^create_category/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<tile_name>[^\\]+)/$', views.CategoryCreateView.as_view(), name='create_category'),
    url(r'^update_category/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<category_name>[^\\]+)/$', views.CategoryUpdateView.as_view(), name='update_category'),
    url(r'^delete_category/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<category_name>[^\\]+)/$', views.CategoryDeleteView.as_view(), name='delete_category'),
    url(r'^create_thing/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<tile_name>[^\\]+)/(?P<category_name>[^\\]+)/$', views.ThingCreateView.as_view(), name='create_thing'),
    url(r'^update_thing/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<category_name>[^\\]+)/(?P<thing_name>[^\\]+)/$', views.ThingUpdateView.as_view(), name='update_thing'),
    url(r'^delete_thing/(?P<pk>[0-9]+)/(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<category_name>[^\\]+)/(?P<thing_name>[^\\]+)/$', views.ThingDeleteView.as_view(), name='delete_thing'),
    url(r'^(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/categories/$', views.category_index, name='category_index'),
    url(r'^(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/category/(?P<category_name>[^\\]+)/$', views.category_detail, name='category_detail'),
    url(r'^(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/tile/(?P<tile_name>[^\\]+)/$', views.tile_detail, name='tile_detail'),
    url(r'^(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/(?P<category_name>[^\\]+)/(?P<thing_name>[^\\]+)/$', views.thing_detail, name='thing_detail'),
    url(r'^(?P<username>[A-Za-z0-9]+)/(?P<world_name>[^\\]+)/$', views.world_detail, name='world_detail'),
    url(r'^(?P<username>[A-Za-z0-9]+)/$', views.world_index, name='world_index'),
    url(r'', views.home, name='forge_home'),
]