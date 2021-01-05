HTTP_OK = 200
REDIRECT = 302

ARTIST_ALBUMS = {
    "album": [
        {
            "idAlbum": "2139279",
            "idArtist": "115909",
            "strAlbum": "Colour the Small One",
            "strArtist": "Sia",
            "intYearReleased": "2004",
            "strAlbumThumb": "https://www.theaudiodb.com/images/media/album/thumb/colour-the-small-one-4f593165326e9.jpg",
            "intScore": "8.3"
        }
    ]
}

ARTIST_DETAILS = {
    "artists": [
        {
            "idArtist": "115909",
            "strArtist": "Sia",
            "strArtistLogo": "https://www.theaudiodb.com/images/media/artist/logo/qyrvtr1582224564.png"
        }
    ]
}

NO_ARTIST = {"album": None}


class TestAlbums:
    ALBUMS_URL = '/albums'

    @staticmethod
    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_no_user(client):
        assert '/connect-page' in client.get(TestAlbums.ALBUMS_URL).location
        assert client.get(TestAlbums.ALBUMS_URL).status_code == REDIRECT

    @staticmethod
    def test_albums_valid_artist(client, db_session, user, mocker):
        TestAlbums.connect(client)
        mock_get_artist_albums = mocker.patch('albumsearcher.audiodb_api.get_artist_albums')
        mock_get_artist_albums.return_value = ARTIST_ALBUMS
        mock_get_artist_details = mocker.patch('albumsearcher.audiodb_api.get_artist_details')
        mock_get_artist_details.return_value = ARTIST_DETAILS
        data = {
            'artist': 'sia'
        }
        resp = client.get(TestAlbums.ALBUMS_URL, query_string=data)
        assert resp.status_code == HTTP_OK
        assert b'Albums results' in resp.data

    @staticmethod
    def test_albums_invalid_artist(client, db_session, user, mocker):
        TestAlbums.connect(client)
        mock_get_artist_albums = mocker.patch('albumsearcher.audiodb_api.get_artist_albums')
        mock_get_artist_albums.return_value = NO_ARTIST
        mock_get_artist_details = mocker.patch('albumsearcher.audiodb_api.get_artist_details')
        mock_get_artist_details.return_value = NO_ARTIST
        data = {
            'artist': 'bla'
        }
        resp = client.get(TestAlbums.ALBUMS_URL, query_string=data)
        assert resp.status_code == REDIRECT
        assert 'valid_artist=false' in resp.location
