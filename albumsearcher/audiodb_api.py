import requests


def get_artist_albums(artist_name):
    url = f'http://theaudiodb.com/api/v1/json/1/searchalbum.php?s={artist_name}'
    return requests.get(url).json()


def get_artist_details(artist_name):
    url = f'http://theaudiodb.com/api/v1/json/1/search.php?s={artist_name}'
    return requests.get(url).json()


def get_album_details(album_id):
    url = f'https://theaudiodb.com/api/v1/json/1/album.php?m={album_id}'
    return requests.get(url).json()


def get_album_tracks(album_id):
    url = f'https://theaudiodb.com/api/v1/json/1/track.php?m={album_id}'
    return requests.get(url).json()


