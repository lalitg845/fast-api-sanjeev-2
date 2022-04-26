from pydoc import cli
import pytest
from jose import jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get('/')
    # print(res.json()['message'])
    assert res.json()['message'] == 'hello world!!'
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        '/users/', json={'email': 'ajay2@gmail.com', 'password': 'ajay2'})

    new_user = schemas.UserOut(**res.json())
    # print(res.json())
    assert new_user.email == 'ajay2@gmail.com'
    assert res.status_code == 201


def test_login_user(test_user, client):
    # print(test_user)
    # print(test_user['password'])

    res = client.post(
        '/login', data={"username": test_user['email'], "password": test_user['password']})

    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key,
                         algorithms=[settings.algorithm])
    # print(payload)
    id: str = payload.get('user_id')
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'

    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", [
    ('ajay@gmail.com', 'wrong', 403),
    ('wrong@gmail.com', 'ajay', 403),
    ('wrong@gmail.com', 'wrong', 403),
    (None, 'ajay', 422),
    ('ajay@gmail.com', None, 422)
])
def test_incorrect_login(email, password, status_code, client):
    res = client.post(
        '/login', data={'username': email, 'password': password})
    assert res.status_code == status_code
    #assert res.json().get('detail') == 'Invalid Credential'
