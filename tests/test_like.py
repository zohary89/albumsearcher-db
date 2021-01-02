from albumsearcher.mapping import Album, Like
from datetime import datetime
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
            "intYearReleased": "1995",
            "intScore": "8",
            "strAlbumThumb": "https://www.theaudiodb.com/images/media/album/thumb/xwvwvp1342551819.jpg",
            }
            ]}

class TestLike:
    LIKE_URL = '/like'
    UNLIKE_URL = '/unlike'

    @staticmethod
    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_like_no_user(client):
        assert '/connect-page' in client.post(TestLike.LIKE_URL).location
    
    @staticmethod
    def test_redirect_unlike_no_user(client):
        assert '/connect-page' in client.post(TestLike.UNLIKE_URL).location

    @staticmethod
    def test_create_like(client, db_session, user, mocker):
        TestLike.connect(client)
        mock_get_album_details = mocker.patch('albumsearcher.audiodb_api.get_album_details')
        mock_get_album_details.return_value = ALBUM_INFO
        data = {
            'idalbum': '2115888'
        }
        resp = client.post(TestLike.LIKE_URL, data=data)
        assert "like=true" in resp.location
        assert db_session.query(Like).filter(Like.user_id == user.user_id).count() == 1
        assert db_session.query(Album).filter(Album.album_id == '2115888').count() == 1

    @staticmethod
    def test_create_unlike(client, user, album, db_session, mocker):
        TestLike.connect(client)
        like = Like(
            user_id=user.user_id, album_id=album.album_id, like_time=datetime.now())
        db_session.add(like)
        db_session.commit()
        album_info_response = ALBUM_INFO
        mock_get_album_details = mocker.patch('albumsearcher.audiodb_api.get_album_details')
        mock_get_album_details.return_value = album_info_response
        data = {
            'idalbum': '2115888'
        }
        resp = client.post(TestLike.UNLIKE_URL, data=data)
        assert "like=false" in resp.location
        assert db_session.query(Like).filter(Like.user_id == user.user_id).count() == 0