import requests
import random
import string
import allure
from data import Urls

def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

class CourierApiHelper:
    @staticmethod
    def generate_courier_login_payload(login, password, name):
        return {"login": login, "password": password, "firstName": name}

    @staticmethod
    @allure.step('Регистрация курьера с помощью логина и пароля.')
    def register_courier(payload):
        return requests.post(Urls.COURIER_HANDLE, data=payload)

    @staticmethod
    @allure.step('Регистрация курьера и возврат списка из логина и пароля.')
    def register_new_courier_and_return_login_password():
        login_pass = []
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = generate_random_string(10)
        response = CourierApiHelper.register_courier(CourierApiHelper.generate_courier_login_payload(login, password, first_name))
        if response.status_code == 201:
            login_pass.extend([login, password, first_name])
        return login_pass

    @staticmethod
    @allure.step('Авторизация курьера с помощью логина и пароля.')
    def login_courier(login: str, password: str):
        return requests.post(Urls.COURIER_LOGIN_HANDLE, json={"login": login, "password": password})

    @staticmethod
    @allure.step('Удаление курьера с помощью id.')
    def delete_courier_by_id(courier_id):
        return requests.delete(f'{Urls.COURIER_HANDLE}/{courier_id}')

    @staticmethod
    @allure.step('Удаление курьера с помощью логина и пароля.')
    def delete_courier_by_login_password(login, password):
        response = requests.post(Urls.COURIER_LOGIN_HANDLE, json={"login": login, "password": password})
        if response.status_code == 200 and 'id' in response.json():
            return CourierApiHelper.delete_courier_by_id(response.json()['id'])
        return response

class OrderApiHelper:
    @staticmethod
    @allure.step('Создание нового заказа.')
    def create_order(first_name: str, last_name: str, address: str, metro_station: int, phone: str, rent_time: int, delivery_date: str, comment: str, color: str):
        return requests.post(Urls.ORDERS_HANDLE, json={"firstName": first_name, "lastName": last_name, "address": address, "metroStation": metro_station,
                                                      "phone": phone, "rentTime": rent_time, "deliveryDate": delivery_date, "comment": comment, "color": [color]})

    @staticmethod
    @allure.step('Принятие заказа.')
    def accept_order(track_order, courier_id):
        return requests.put(f'{Urls.ORDERS_ACCEPT_HANDLE}?courierId={courier_id}', json={"track": track_order})

    @staticmethod
    @allure.step('Получение списка заказов.')
    def request_orders_list():
        return requests.get(Urls.ORDERS_HANDLE)

    @staticmethod
    @allure.step('Получение заказа по его номеру.')
    def request_order_by_track(track):
        return requests.get(f'{Urls.ORDERS_GET_BY_TRACK_HANDLE}?t={track}')

    @staticmethod
    @allure.step('Отмена заказа.')
    def cancel_order(track_order):
        return requests.put(Urls.ORDERS_CANCEL_HANDLE, json={"track": track_order})
