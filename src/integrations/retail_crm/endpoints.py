from typing import NamedTuple


class Endpoint(NamedTuple):
    path: str
    method: str


class RetailCRMEndpoint:
    GET_CUSTOMERS = Endpoint(path='customers', method='GET')
    CREATE_CUSTOMER = Endpoint(path='customers/create', method='POST')
    GET_ORDERS = Endpoint(path='orders', method='GET')
    CREATE_ORDER = Endpoint(path='orders/create', method='POST')
    CREATE_PAYMENT_FOR_ORDER = Endpoint(path='orders/payments/create', method='POST')
