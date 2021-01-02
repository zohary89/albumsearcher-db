from albumsearcher.mapping import User
import pytest

HTTP_OK = 200
NOT_ALLOWED = 405

POSSIBLE_MISSING_FIELD = [
    ('', '', '', '', ''),
    ('dani', '', '', '1.11.1990', 'israel'),
]

class TestRegister:
    REGISTER = '/register-page'
    REGISTER_POST = '/register'
    SECCESS = '/connect-page'
    USER_EXIST = 'user_exist=true'

    @staticmethod
    def test_register_get_page(client):
        assert client.get(TestRegister.REGISTER).status_code == HTTP_OK
    
    @staticmethod
    def test_register_no_page(client):
        assert client.get(TestRegister.REGISTER_POST).status_code == NOT_ALLOWED

    @staticmethod
    def test_create_user_successfully(client, db_session):
        data = {
            'user-name': 'zohar',
            'psw': '12345',
            'name': 'zohar',
            'birthday': '01.11.1989',
            'country': 'Israel'
        }
        resp = client.post(TestRegister.REGISTER_POST, data=data)
        new_user = db_session.query(User).filter(User.username == 'zohar').first()
        assert new_user.username == 'zohar'
        assert new_user.name == 'zohar'
        assert new_user.birthday == '01.11.1989'
        assert new_user.country == 'Israel'
        assert TestRegister.SECCESS in resp.location

    @staticmethod
    def test_username_exist(client, user):
        data = {
            'user-name': 'dani',
            'psw': '123456',
            'name': 'daniel',
            'birthday': '01.04.1995',
            'country': 'israel'
        }
        resp = client.post(TestRegister.REGISTER_POST, data=data)
        assert TestRegister.USER_EXIST and TestRegister.REGISTER in resp.location

    @staticmethod
    @pytest.mark.parametrize("username, password, name, birthday, country", POSSIBLE_MISSING_FIELD)
    def test_register_fields_are_empty(client, username, password, name, birthday, country):
        data = {
            'user-name': username,
            'psw': password,
            'name': name,
            'birthday': birthday,
            'country': country
        }        
        resp = client.post(TestRegister.REGISTER_POST, data=data)
        assert TestRegister.REGISTER in resp.location
