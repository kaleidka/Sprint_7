import allure
import pytest
from helpers import CourierApiHelper, generate_random_string
from data import Responses

class TestLoginCourier:
    @allure.title('Авторизация зарегистрированного курьера')
    def test_login_courier(self, create_courier):
        login = create_courier[0]
        password = create_courier[1]
        response = CourierApiHelper.login_courier(login, password)
        assert response.status_code == 200 and 'id' in response.json()

    @allure.title('Авторизация курьера без логина или пароля')
    @pytest.mark.parametrize("login, password", [
        ('', generate_random_string(10)),
        (generate_random_string(10), '')
    ])
    def test_login_courier_no_login_no_password(self, login, password):
        response = CourierApiHelper.login_courier(login, password)
        assert response.status_code == 400 and response.json() == Responses.CODE_400_LOGIN_COURIER

    @allure.title('Авторизация курьера с некорректным логином или паролем')
    @pytest.mark.parametrize("login, password", [
        (True, False),
        (False, True)
    ])
    def test_login_courier_incorrect_login_password(self, create_courier, login, password):
        login = create_courier[0] if login else 'test_login'
        password = create_courier[1] if password else 'test_password'
        response = CourierApiHelper.login_courier(login, password)
        assert response.status_code == 404 and response.json() == Responses.CODE_404_LOGIN_COURIER
