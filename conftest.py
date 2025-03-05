import pytest
from helpers import CourierApiHelper, OrderApiHelper, generate_random_string
from data import OrderData

@pytest.fixture
def create_courier():
    register = CourierApiHelper.register_new_courier_and_return_login_password()
    yield register
    CourierApiHelper.delete_courier_by_login_password(register[0], register[1])

@pytest.fixture
def login_info():
    login = generate_random_string(10)
    password = generate_random_string(9)
    name = generate_random_string(8)
    login_info = CourierApiHelper.generate_courier_login_payload(login, password, name)
    yield login_info
    CourierApiHelper.delete_courier_by_login_password(login, password)

@pytest.fixture
def login_courier(create_courier):
    response = CourierApiHelper.login_courier(create_courier[0], create_courier[1])
    if response.status_code == 200 and 'id' in response.json():
        courier_id = response.json()['id']
        yield courier_id
    else:
        yield None

@pytest.fixture
def create_order():
    response = OrderApiHelper.create_order(generate_random_string(11), generate_random_string(11),
                                           OrderData.address, OrderData.metro_station, OrderData.phone,
                                           OrderData.rent_time, OrderData.delivery_date, OrderData.comment, OrderData.color_black)
    if response.status_code == 201 and 'track' in response.json():
        track_order = response.json()['track']
        yield track_order
        OrderApiHelper.cancel_order(track_order)
    else:
        yield None
