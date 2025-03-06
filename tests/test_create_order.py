import allure
import pytest
from helpers import OrderApiHelper, generate_random_string
from data import OrderData

class TestCreateOrder:
    @allure.title('Создание заказа с различными цветами самоката')
    @pytest.mark.parametrize("color", [
        OrderData.color_black,
        OrderData.color_grey,
        OrderData.color_black_grey,
        OrderData.color_empty
    ])
    def test_create_new_order(self, color):
        order_helper = OrderApiHelper()
        response = order_helper.create_order(generate_random_string(11), generate_random_string(11),
                                             OrderData.address, OrderData.metro_station, OrderData.phone,
                                             OrderData.rent_time, OrderData.delivery_date, OrderData.comment, color)
        assert response.status_code == 201 and 'track' in response.json()
