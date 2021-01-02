HTTP_OK = 200
REDIRECT = 302


class TestUpdate:
    UPDATE_URL = '/update'
    USER_EXIST = 'user_exist=true'

    def connect(client):
        data = {
            'user-name': 'dani',
            'psw': '1234'
        }
        client.post('/connect', data=data)

    @staticmethod
    def test_redirect_no_user(client):
        assert '/connect-page' in client.get(TestUpdate.UPDATE_URL).location
        assert client.get(TestUpdate.UPDATE_URL).status_code == REDIRECT

    @staticmethod
    def test_get_update_page(client, user):
        TestUpdate.connect(client)
        assert client.get(TestUpdate.UPDATE_URL).status_code == HTTP_OK

    @staticmethod
    def test_update_success(client, user):
        TestUpdate.connect(client)
        data = {
            'user-name': 'daniel',
            'name': 'daniel',
            'birthday': '02.11.1990',
            'country': 'israel'
        }
        resp = client.post(TestUpdate.UPDATE_URL, data=data, follow_redirects=True)
        assert b'daniel' in resp.data
        data2 = {
            'user-name': 'daniel',
            'psw': '1234',
            }
        resp2 = client.post('/connect', data=data2, follow_redirects=True)  # בדיקה שמתחבר עם שם המשתמש החדש לאחר עדכון פרטים.
        assert b'daniel' in resp.data

    @staticmethod
    def test_fail_update(client, user):
        TestUpdate.connect(client)
        data = {
            'user-name': 'zohar',     # הכנסת משתמש חדש למערכת
            'psw': '12345',
            'name': 'zohar',
            'birthday': '01.11.1989',
            'country': 'israel'
        }
        client.post('/register', data=data)   
        data2 = {
            'user-name': 'zohar',     # ניסיון עדכון לשם שקיים במערכת
            'name': 'zohar',
            'birthday': '02.11.1990',
            'country': 'israel'
        }
        resp = client.post(TestUpdate.UPDATE_URL, data=data2)
        assert TestUpdate.UPDATE_URL and TestUpdate.USER_EXIST in resp.location 