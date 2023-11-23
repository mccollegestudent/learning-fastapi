from app import schemas
from jose import jwt             #validation
from app.config import settings
import pytest

def test_root(client):
    res = client.get("/") #we dont need the root we just use the app instance since its not a server etc
    print(res.json().get('message'))
    assert res.json().get('message') == 'Welcome to my api testing in progress'

def test_create_user(client):
    res = client.post("/users", json={"email":"hello@gmail.com", "password":"1234"})
    new_user = schemas.UserOut(**res.json()) # **sd have to unpack
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username":test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())  #spread res perfoms some validation    -> we also need to validate this token

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id =  payload.get("user_id") #extract id

    assert id == test_user['id'] #valid check
    assert login_res.token_type == 'bearer'
    assert res.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
                        ("user123@example.com", "passw0rd!", 403),
                        ("john_doe@gmail.com", "securePwd123", 403),
                        ("test_user@hotmail.com", "P@ssw0rd", 403),
                        (None, "1234abcd", 422),
                        ("demo_user@example.org", None, 422)
                        ])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("login", data={"username":email, "password": password})
    assert res.status_code == status_code


