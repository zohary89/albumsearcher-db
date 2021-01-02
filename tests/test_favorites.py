HTTP_OK = 200
REDIRECT = 302


class TestFavorites:
    FAVORITES_URL = '/favorites'

    @staticmethod
    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_favorites_no_user(client):
        assert '/connect-page' in client.get(TestFavorites.FAVORITES_URL).location
        assert client.get(TestFavorites.FAVORITES_URL).status_code == REDIRECT

    @staticmethod
    def test_get_1_favorite(client, user, like):
        TestFavorites.connect(client)
        resp = client.get(TestFavorites.FAVORITES_URL)
        assert resp.status_code == HTTP_OK
        assert b'Total liked albums: 1' in resp.data

    @staticmethod
    def test_get_2_favorites(client, user, like, like2):
        TestFavorites.connect(client)
        resp = client.get(TestFavorites.FAVORITES_URL)
        assert resp.status_code == HTTP_OK
        assert b'Total liked albums: 2' in resp.data
       
    @staticmethod
    def test_get_no_favorites(client, user):
        TestFavorites.connect(client)
        resp = client.get(TestFavorites.FAVORITES_URL)
        assert resp.status_code == HTTP_OK
        assert b"You haven't selected your favorite albums yet" in resp.data
