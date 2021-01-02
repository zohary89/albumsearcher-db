HTTP_OK = 200
REDIRECT = 302


class TestIndex:
    INDEX_URL = '/'

    @staticmethod
    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_index_no_user(client):
        assert '/connect-page' in client.get(TestIndex.INDEX_URL).location
        assert client.get(TestIndex.INDEX_URL).status_code == REDIRECT

    @staticmethod
    def test_index_no_top_liked(client, user):
        TestIndex.connect(client)
        resp = client.get(TestIndex.INDEX_URL)
        assert resp.status_code == HTTP_OK
        assert b'Top 10 Liked Albums' not in resp.data

    @staticmethod
    def test_index_top_likes(client, user, like, like2):
        TestIndex.connect(client)
        resp = client.get(TestIndex.INDEX_URL)
        assert resp.status_code == HTTP_OK
        assert b'Top 10 Liked Albums' in resp.data