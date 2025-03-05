import allure
import pytest
from helpers import OrderApiHelper, generate_random_string
from data import OrderData, Responses

class TestCreateOrder:
    @allure.title('Создание заказа с различными цветами самоката')
    @pytest.mark.parametrize("color", [
        OrderData.color_black,
        OrderData.color_grey,
        OrderData.color_black_grey,
        OrderData.color_empty
    ])
    def test_create_new_order(self, color):
        response = OrderApiHelper.create_order(generate_random_string(11), generate_random_string(11),
                                               OrderData.address, OrderData.metro_station, OrderData.phone,
                                               OrderData.rent_time, OrderData.delivery_date, OrderData.comment, color)
        assert response.status_code == 201 and 'track' in response.json()
        track_order = response.json()['track']
        OrderApiHelper.cancel_order(track_order)

class TestGetOrder:
    @allure.title('Получение списка заказов')
    def test_request_orders_list(self):
        response = OrderApiHelper.request_orders_list()
        assert response.status_code == 200 and 'orders' in response.json()

    @allure.title('Получение заказа по его номеру')
    def test_get_order_by_track(self, create_order):
        track_id = create_order
        if track_id:
            response = OrderApiHelper.request_order_by_track(track_id)
            assert response.status_code == 200 and response.json()['order']['track'] == track_id

    @allure.title('Получение заказа без указания номера')
    def test_get_order_by_empty_track(self):
        response = OrderApiHelper.request_order_by_track('')
        assert response.status_code == 400 and response.json() == Responses.CODE_400_GET_ORDER_BY_EMPTY_TRACK

    @allure.title('Получение заказа с несуществующим номером')
    def test_get_order_by_incorrect_track(self):
        response = OrderApiHelper.request_order_by_track(666666666)
        assert response.status_code == 404 and response.json() == Responses.CODE_404_GET_ORDER_BY_INCORRECT_TRACK

class TestAcceptOrder:
    @allure.title('Принятие заказа курьером')
    def test_accept_order(self, login_courier, create_order):
        courier_id = login_courier
        order_id = create_order
        if courier_id and order_id:
            response = OrderApiHelper.accept_order(order_id, courier_id)
            assert response.status_code == 200 and response.json() == {'ok': True}

    @allure.title('Принятие заказа без id курьера или id заказа')
    @pytest.mark.parametrize("courier_id, order_id", [
        (False, True),
        (True, False)
    ])
    def test_accept_order_no_login_no_password(self, login_courier, create_order, courier_id, order_id):
        courier_id = login_courier if courier_id else ''
        order_id = create_order if order_id else ''
        response = OrderApiHelper.accept_order(order_id, courier_id)
        assert response.status_code == 400 and response.json() == Responses.CODE_400_ACCEPT_ORDER

    @allure.title('Принятие заказа с несуществующим id курьера или id заказа')
    @pytest.mark.parametrize("courier_id, order_id, message", [
        (False, True, Responses.CODE_404_ACCEPT_ORDER_INCORRECT_COURIER_ID),
        (True, False, Responses.CODE_404_ACCEPT_ORDER_INCORRECT_ORDER_ID)
    ])
    def test_accept_order_incorrect_login_incorrect_password(self, login_courier, create_order, courier_id, order_id, message):
        courier_id = login_courier if courier_id else '66666666'
        order_id = create_order if order_id else '666666666'
        response = OrderApiHelper.accept_order(order_id, courier_id)
        assert response.status_code == 404 and response.json() == message
