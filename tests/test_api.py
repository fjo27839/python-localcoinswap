import pytest
import requests_mock

from localcoinswap.client import Client
from localcoinswap.exceptions import (LocalcoinswapAPIException,
                                      LocalcoinswapResponseException)

# Set get_params=False, otherwise client will try to set
# them up and fail the authentication
client = Client('api_token', get_params=False)

def test_api_exception_json():
    '''
    Test API response exception (non-2xx status code).
    JSON response.
    '''

    with pytest.raises(LocalcoinswapAPIException):
        with requests_mock.mock() as m:
            json_resp = {'error': True,
                         'code': 'invalid_user',
                         'message': 'Not found'}
            m.get(client.create_api_url('new-trade/'),
                json=json_resp,
                status_code=400)
            client.get_trade_params()

def test_api_exception_text():
    '''
    Test API response exception (non-2xx status code).
    Non-JSON response.
    '''

    with pytest.raises(LocalcoinswapAPIException):
        with requests_mock.mock() as m:
            m.get(client.create_api_url('new-trade/'),
                text='<html>Not Found</html>',
                status_code=404)
            client.get_trade_params()

def test_response_exception():
    '''
    Test Response exception (non-json response when json was excepted).
    '''

    with pytest.raises(LocalcoinswapResponseException):
        with requests_mock.mock() as m:
            m.get(client.create_api_url('new-trade/'),
                  text='Trade params: 1,2,3',
                  status_code=200)
            client.get_trade_params()
