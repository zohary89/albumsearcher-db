from pytest_mock import mocker

HTTP_OK = 200
REDIRECT = 302

ALBUM_INFO = {
    "album": [
        {
            "idAlbum": "2115888",
            "idArtist": "112024",
            "strAlbum": "Echoes of Silence",
            "strArtist": "The Weeknd",
            "strAlbumThumb": "https://www.theaudiodb.com/images/media/album/thumb/xwvwvp1342551819.jpg",
            "strDescriptionEN": "........."
            }
            ]}

TRACKS = {
    "track":[
        {
            "idTrack":"32793500",
            "idAlbum":"2115888",
            "strTrack":"D.D."
            },
        {
            "idTrack":"32793501",
            "idAlbum":"2115888",
            "strTrack":"Montreal"
            }
            ]}

NO_ALBUM = {"album": None}


class TestAlbumInfo:
    ALBUM_URL = '/albums/2115888'

    @staticmethod
    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_no_user(client):
        assert '/connect-page' in client.get(TestAlbumInfo.ALBUM_URL).location
        assert client.get(TestAlbumInfo.ALBUM_URL).status_code == REDIRECT


    @staticmethod
    def test_info_valid_album(client, db_session, user, mocker):
        TestAlbumInfo.connect(client)
        mock_get_album_details = mocker.patch('albumsearcher.audiodb_api.get_album_details')
        mock_get_album_details.return_value = ALBUM_INFO
        mock_get_album_tracks = mocker.patch('albumsearcher.audiodb_api.get_album_tracks')
        mock_get_album_tracks.return_value = TRACKS
        resp = client.get(TestAlbumInfo.ALBUM_URL)
        assert resp.status_code == HTTP_OK
        assert b'Album info' in resp.data
        mock_get_album_details.assert_called_once_with("2115888")

    @staticmethod
    def test_info_invalid_album(client, db_session, user, mocker):
        TestAlbumInfo.connect(client)
        mock_get_album_details = mocker.patch('albumsearcher.audiodb_api.get_album_details')
        mock_get_album_details.return_value = NO_ALBUM
        resp = client.get(TestAlbumInfo.ALBUM_URL)
        assert resp.status_code == REDIRECT
        assert resp.location == 'http://localhost/'


    @staticmethod
    def test_info_valid_album_with_like(client, db_session, user, album, like, mocker):
        TestAlbumInfo.connect(client)
        mock_get_album_details = mocker.patch('albumsearcher.audiodb_api.get_album_details')
        mock_get_album_details.return_value = ALBUM_INFO
        mock_get_album_tracks = mocker.patch('albumsearcher.audiodb_api.get_album_tracks')
        mock_get_album_tracks.return_value = TRACKS
        resp = client.get(TestAlbumInfo.ALBUM_URL)
        assert resp.status_code == HTTP_OK
        assert b'Total likes: 1' in resp.data