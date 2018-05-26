from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import AlbumForm, SongForm
from .models import Album, Songs
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import Http404
from django.views.generic.edit import DeleteView

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']


def index(request):
    albums = Album.objects.all()
    song_results = Songs.objects.all()
    query = request.GET.get("q")
    if query:
        album = albums.filter(
            Q(album_title__icontains=query) |
            Q(artist__icontains=query)
        ).distinct()
        song_results = song_results.filter(
        Q(song_title__icontains=query)
        ).distinct()
        return render(request, 'music/index.html', {
            'all_album': album,
            'songs': song_results,
        })
    else:
        return render(request, 'music/index.html', {'all_album': albums})

def details(request,album_id):
    try:
        album=Album.objects.get(pk=album_id)
    except Album.DoesNotExist:
        raise Http404("Album does not request")
    return render(request, 'music/detail.html', {'album':album})

def favourite(request,song_id):
    song = get_object_or_404(Songs, pk=song_id)

    if song.is_favorite:
            song.is_favorite = False
    else:
            song.is_favorite = True
    song.save()


def createalbum(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        album = form.save(commit=False)
        album.user = request.user
        album.album_logo = request.FILES['album_logo']
        file_type = album.album_logo.url.split('.')[-1]
        file_type = file_type.lower()
        album.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        "form": form,
    }
    return render(request, 'music/album_form.html', context)


def create_song(request, album_id):
    form = SongForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_songs = album.songs_set.all()
        for s in albums_songs:
            if s.song_title == form.cleaned_data.get("song_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that song',
                }
                return render(request, 'music/create_song.html', context)
        song = form.save(commit=False)
        song.album = album
        song.file_type = request.FILES['file_type']
        file = song.file_type.url.split('.')[-1]
        file = file.lower()
        if file not in AUDIO_FILE_TYPES:
            context = {
                'album': album,
                'form': form,
                'error_message': 'Audio file must be WAV, MP3, or OGG',
            }
            return render(request, 'music/create_song.html', context)

        song.save()
        return render(request, 'music/detail.html', {'album': album})
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'music/create_song.html', context)


def delete_song(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Songs.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album': album})


def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    album = Album.objects.all()
    context = {'all_album': album}
    return render(request,'music/index.html',context)


def songs(request):
    song_ids = []
    for album in Album.objects.all():
        for song in album.songs_set.all():
            song_ids.append(song.pk)

    users_songs = Songs.objects.filter(pk__in=song_ids)

    return render(request, 'music/song.html', {
            'song_list':users_songs,
    })
