from flask import session
import pytest

HTTP_OK = 200
NOT_ALLOWED = 405

POSSIBLE_MISSING_FIELD = [
    ('', ''),
    ('israel', ''),
    ('', '1234')
]


class TestLogin:
    LOGIN = '/connect-page'
    LOGIN_POST = '/connect'
    LOGIN_FAILED = 'login_failed=true'

    @staticmethod
    def test_connect_get_page(client):
        assert client.get(TestLogin.LOGIN).status_code == HTTP_OK
    
    @staticmethod
    def test_connect_no_page(client):
        assert client.get(TestLogin.LOGIN_POST).status_code == NOT_ALLOWED

    @staticmethod
    @pytest.mark.parametrize("username, password", POSSIBLE_MISSING_FIELD)
    def test_login_fields_are_empty(client, username, password):
        data = {'user-name': username, 'psw': password}
        resp = client.post(TestLogin.LOGIN_POST, data=data)
        assert (TestLogin.LOGIN and TestLogin.LOGIN_FAILED) in resp.location

    @staticmethod
    def test_login_details_are_absolutly_wrong(client):
        data = {
            'user-name': 'zohar',
            'psw': '12345',
        }
        resp = client.post(TestLogin.LOGIN_POST, data=data)
        assert TestLogin.LOGIN_FAILED in resp.location

    @staticmethod
    def test_login_successfully(client, user):
        data = {
            'user-name': 'dani',
            'psw': '1234',
        }
        resp = client.post(TestLogin.LOGIN_POST, data=data)
        assert session['user_id'] == user.user_id
        assert resp.location == 'http://localhost/'

    @staticmethod
    def test_incorrect_password(client, user):
        data = {
            'user-name': 'dani',
            'psw': '12345',
        }
        resp = client.post(TestLogin.LOGIN_POST, data=data)
        assert TestLogin.LOGIN_FAILED in resp.location
