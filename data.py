class Urls:
    HOME_URL = 'http://qa-scooter.praktikum-services.ru/'
    COURIER_HANDLE = f'{HOME_URL}api/v1/courier'
    COURIER_LOGIN_HANDLE = f'{COURIER_HANDLE}/login'
    ORDERS_HANDLE = f'{HOME_URL}api/v1/orders'
    ORDERS_CANCEL_HANDLE = f'{ORDERS_HANDLE}/cancel'
    ORDERS_ACCEPT_HANDLE = f'{ORDERS_HANDLE}/accept'
    ORDERS_GET_BY_TRACK_HANDLE = f'{ORDERS_HANDLE}/track'

class Responses:
    CODE_400_CREATE_COURIER = {'code': 400, 'message': 'Недостаточно данных для создания учетной записи'}
    CODE_409_CREATE_COURIER = {'code': 409, 'message': 'Этот логин уже используется. Попробуйте другой.'}
    CODE_400_LOGIN_COURIER = {'code': 400, 'message': 'Недостаточно данных для входа'}
    CODE_404_LOGIN_COURIER = {'code': 404, 'message': 'Учетная запись не найдена'}
    CODE_400_DELETE_COURIER = {'code': 404, 'message': 'Not Found.'}
    CODE_404_DELETE_COURIER = {'code': 404, 'message': 'Курьера с таким id нет.'}
    CODE_400_ACCEPT_ORDER = {'code': 400, 'message': 'Недостаточно данных для поиска'}
    CODE_404_ACCEPT_ORDER_INCORRECT_COURIER_ID = {'code': 404, 'message': 'Курьера с таким id не существует'}
    CODE_404_ACCEPT_ORDER_INCORRECT_ORDER_ID = {'code': 404, 'message': 'Заказа с таким id не существует'}
    CODE_400_GET_ORDER_BY_EMPTY_TRACK = {'code': 400, 'message': 'Недостаточно данных для поиска'}
    CODE_404_GET_ORDER_BY_INCORRECT_TRACK = {'code': 404, 'message': 'Заказ не найден'}

class OrderData:
    address = "Konoha, 142 apt."
    metro_station = 4
    phone = "+7 800 355 35 35"
    rent_time = 5
    delivery_date = "2020-06-06"
    comment = "Saske, come back to Konoha"
    color_black = "BLACK"
    color_grey = "GREY"
    color_black_grey = "BLACK, GREY"
    color_empty = ""
