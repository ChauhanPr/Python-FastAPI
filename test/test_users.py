
from .utils import *
from routers.users import get_db, get_current_user
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] == override_get_current_user

def test_return_user(user_test):
    response = client.get("/users")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'preetichauhan'
    assert response.json()['email'] == 'preet@gmail.com'
    assert response.json()['first_name'] == 'Preeti'
    assert response.json()['last_name'] == 'Chauhan'
    assert response.json()['role'] == 'admin'

def test_change_password_success(user_test):
    response = client.put("/users/password",json={"password": "preet123",
                                                 "new_password": "newpassword"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(user_test):
    response = client.put("/users/password",json={"password": "wrong_password",
                                                 "new_password": "newpassword"})
    assert response.status_code == 401
    assert response.json() == {'detail':'Error on Password Change'}


    

    
