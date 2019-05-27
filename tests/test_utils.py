import pytest

from localcoinswap.utils import (get_crypto_currency_id,
                                 get_fiat_currency_id,
                                 get_payment_method_id,
                                 get_trade_type_id)
from localcoinswap.exceptions import LocalcoinswapInvalidParamError

from .sample_data import trade_params

def test_get_crypto_currency_id():
    '''
    Test utils.get_currency_id (from id, name or title)
    '''

    assert get_crypto_currency_id(trade_params, 'BTC') == 1
    assert get_crypto_currency_id(trade_params, '1') == 1
    assert get_crypto_currency_id(trade_params, 'btc') == 1
    assert get_crypto_currency_id(trade_params, 'Ethereum') == 2
    assert get_crypto_currency_id(trade_params, 2) == 2
    assert get_crypto_currency_id(trade_params, 'eTh') == 2
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_crypto_currency_id(trade_params, 'USD')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_crypto_currency_id({'payment_method': 123}, 'btc')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_crypto_currency_id(None, 'eth')

def test_get_fiat_currency_id():
    '''
    Test utils.get_currency_id (from id, name or title)
    '''

    assert get_fiat_currency_id(trade_params, 'uNited sTates dOllar') == 10001
    assert get_fiat_currency_id(trade_params, '10001') == 10001
    assert get_fiat_currency_id(trade_params, 'usd') == 10001
    assert get_fiat_currency_id(trade_params, 10003) == 10003
    assert get_fiat_currency_id(trade_params, 'Eur') == 10003
    assert get_fiat_currency_id(trade_params, 'EUR') == 10003
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_fiat_currency_id(trade_params, 'xrp')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_fiat_currency_id({'payment_method': 123}, 'eur')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_fiat_currency_id(None, 'eth')

def test_get_payment_method_id():
    '''
    Test utils.get_payment_method_id (from id or name)
    '''

    assert get_payment_method_id(trade_params, '1') == 1
    assert get_payment_method_id(trade_params, 'Local Bank transfer') == 1
    assert get_payment_method_id(trade_params, 2) == 2
    assert get_payment_method_id(trade_params, 'cash depoSit') == 2
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_payment_method_id(trade_params, 'my imaginary method')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_payment_method_id({'fiat_currency': [1,2,3]}, 'my imaginary method')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_payment_method_id(None, 'I want to believe')

def test_get_trade_type_id():
    '''
    Test utils.get_trade_type_id (from id, name or action name).
    '''

    assert get_trade_type_id(trade_params, 1) == 1
    assert get_trade_type_id(trade_params, 'Buy') == 1
    assert get_trade_type_id(trade_params, 'buying') == 1
    assert get_trade_type_id(trade_params, 'SELL') == 2
    assert get_trade_type_id(trade_params, '2') == 2
    assert get_trade_type_id(trade_params, 'sell') == 2
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_trade_type_id(trade_params, 'converting')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_trade_type_id({'currency': {'btc': 1}}, 'Buy')
    with pytest.raises(LocalcoinswapInvalidParamError):
        get_trade_type_id(None, 'sell')
