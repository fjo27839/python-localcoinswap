from .exceptions import LocalcoinswapInvalidParamError

'''
Util functions (various type/name converts)
'''

def get_crypto_currency_id(trade_params, currency):
    """
    Finds crypto currency id in trade_params for currency in
    arguments (id, name or symbol) to use in API requests.

    :param dict trade_params: trade params from client (see
                              ``client.get_trade_params`` &
                              ``client.set_trade_params``)
    :param int/str currency: currency name, symbol or id
    :returns: currency id
    :rtype: int

    :raises: LocalcoinswapInvalidParamError

    """

    # if trade_params are not set up/passed, this fails
    if trade_params and 'crypto_currencies' in trade_params:
        for c in trade_params['crypto_currencies']:
            if str(currency) == str(c['id']) or str(currency).lower() in [c['title'].lower(), c['symbol'].lower()]:
                return c['id']
        raise LocalcoinswapInvalidParamError('Invalid crypto currency \'{}\''.format(currency))
    raise LocalcoinswapInvalidParamError('trade_params are not set up')

def get_fiat_currency_id(trade_params, currency):
    """
    Finds fiat currency id in trade_params for currency in
    arguments (id, name or symbol) to use in API requests.

    :param dict trade_params: trade params from client (see
                              ``client.get_trade_params`` &
                              ``client.set_trade_params``)
    :param int/str currency: currency name, symbol or id
    :returns: currency id
    :rtype: int

    :raises: LocalcoinswapInvalidParamError

    """

    # if trade_params are not set up/passed, this fails
    if trade_params and 'fiat_currencies' in trade_params:
        for c in trade_params['fiat_currencies']:
            if str(currency) == str(c['id']) or str(currency).lower() in [c['title'].lower(), c['symbol'].lower()]:
                return c['id']
        raise LocalcoinswapInvalidParamError('Invalid fiat currency \'{}\''.format(currency))
    raise LocalcoinswapInvalidParamError('trade_params are not set up')

def get_payment_method_id(trade_params, method):
    """
    Finds payment method id in trade_params that corresponds to
    method argument (id or name) to use in API requests.

    :param dict trade_params: trade params from client (currencies, types, etc.)
    :param int/str method: payment method name or id
    :returns: payment method id
    :rtype: int

    :raises: LocalcoinswapInvalidParamError

    """

    if trade_params and 'payment_methods' in trade_params:
        for pm in trade_params['payment_methods']:
            if str(method) == str(pm['id']) or str(method).lower() == pm['name'].lower():
                return pm['id']
        raise LocalcoinswapInvalidParamError('Invalid payment method \'{}\''.format(method))
    raise LocalcoinswapInvalidParamError('trade_params are not set up')

def get_trade_type_id(trade_params, trade_type):
    """
    Find trade type id (1 or 2) in trade_params that corresponds to
    trade_type argument (id, name or action name) to use in API requests.

    :param dict trade_params: trade params from client (currencies, types, etc.)
    :param int/str trade_type: trading type name, action name or id
    :returns: trading type id
    :rtype: int

    :raises: LocalcoinswapInvalidParamError

    """

    if trade_params and 'trade_types' in trade_params:
        for t in trade_params['trade_types']:
            if str(trade_type) == str(t['id']) or str(trade_type).lower() in [t['name'].lower(), t['action_name'].lower()]:
                return t['id']
        raise LocalcoinswapInvalidParamError('Invalid trade type \'{}\''.format(trade_type))
    raise LocalcoinswapInvalidParamError('trade_params are not set up')
