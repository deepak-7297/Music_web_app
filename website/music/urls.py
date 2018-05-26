from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    #music/album_id
    path('<int:album_id>/',views.details,name='detail'),
    #music/album_id/favourite
    path('favourite/<int:song_id>', views.favourite, name='favourite'),
    path('add',views.createalbum,name='create_album'),
    path('<int:album_id>/delete',views.delete_album,name='delete_album'),
    path('<int:album_id>/createsong',views.create_song,name='create_song'),
    path('<int:album_id>/deletesong/<int:song_id>',views.delete_song,name='delete_song'),
    path('songs', views.songs, name='songs')
]