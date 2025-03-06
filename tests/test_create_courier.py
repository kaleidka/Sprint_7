import allure
import pytest
from helpers import CourierApiHelper, generate_random_string
from data import Responses

class TestCreateCourier:
    @allure.title('Создание нового курьера')
    def test_create_new_courier(self, login_info):
        courier_helper = CourierApiHelper()
        response = courier_helper.register_courier(login_info)
        assert response.status_code == 201 and response.json() == {'ok': True}

    @allure.title('Создание двух одинаковых курьеров')
    def test_create_two_same_couriers(self, login_info):
        courier_helper = CourierApiHelper()
        courier_helper.register_courier(login_info)
        response = courier_helper.register_courier(login_info)
        assert response.status_code == 409 and response.json() == Responses.CODE_409_CREATE_COURIER

    @allure.title('Создание курьера без логина или пароля')
    @pytest.mark.parametrize("login, password, name", [
        ('', generate_random_string(10), generate_random_string(10)),
        (generate_random_string(10), '', generate_random_string(10))
    ])
    def test_create_courier_no_login_no_password_no_name(self, login, password, name):
        courier_helper = CourierApiHelper()
        response = courier_helper.register_courier(courier_helper.generate_courier_login_payload(login, password, name))
        assert response.status_code == 400 and response.json() == Responses.CODE_400_CREATE_COURIER

class TestDeleteCourier:
    @allure.title('Удаление существующего курьера')
    def test_delete_courier(self):
        courier_helper = CourierApiHelper()
        courier = courier_helper.register_new_courier_and_return_login_password()
        response = courier_helper.delete_courier_by_login_password(courier[0], courier[1])
        assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Удаление курьера без указания id')
    def test_delete_courier_without_id(self):
        courier_helper = CourierApiHelper()
        response = courier_helper.delete_courier_by_id('')
        assert response.status_code == 404 and response.json() == Responses.CODE_400_DELETE_COURIER

    @allure.title('Удаление курьера с несуществующим id')
    def test_delete_courier_no_login_no_password_no_name(self):
        courier_helper = CourierApiHelper()
        response = courier_helper.delete_courier_by_id(99999999)
        assert response.status_code == 404 and response.json() == Responses.CODE_404_DELETE_COURIER
