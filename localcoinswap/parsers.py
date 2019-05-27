'''
Parse API responses for relevant data.
'''

def parse_wallet(data):
    """
    Parses relevant fields from wallets (list of dicts).

    :param list data: list of wallet dictionaries
    :returns: parsed list of wallet dictionaries
    :rtype: list
    """

    return [{
            'name': wallet['currency']['title'],
            'symbol': wallet['currency']['symbol'],
            'id': wallet['currency']['id'],
            'coin_amount': float(wallet['amount']),
            'fiat_amount': float(wallet['amount_in_local_currency']['amount_in_local_currency']),
            'fiat_currency': wallet['amount_in_local_currency']['local_currency_symbol'],
            'address': wallet['address']['address'],
            'payment_id': wallet['address']['chip']
            } for wallet in data]

def parse_deposit_address(data):
    """
    Parses relevant fields from deposit address data.

    :param data: address info for one currency (address)
    :type data: dict
    :returns: parsed data for currency
    :rtype: dict
    """

    return {
        'name': data['currency']['title'],
        'symbol': data['currency']['symbol'],
        'balance': float(data['amount']),
        'address': data['address']['address'],
        'payment_id': data['address']['chip']
    }

def parse_transaction(transaction):
    """
    Parsed relevant fields from transaction data.

    :param transaction: transaction data
    :type transaction: dict
    :returns: parsed transaction data
    :rtype: dict
    """

    _from = transaction['from_user']['username'] if transaction['from_user'] else ''
    if transaction['transaction_type'] in ['contract_escrow',
                                           'contract_escrow_revert',
                                           'contract_escrow_release']:
        _to = transaction['to_user']['username']
    else:
        _to = transaction['to_address'] if transaction['to_address'] else ''

    return {
        'transaction_type': transaction['transaction_type'],
        'amount': transaction['amount'],
        'currency': transaction['currency']['symbol'],
        'timestamp': transaction['timestamp'],
        'from': _from,
        'to': _to
    }

def parse_transactions(data):
    """
    Processes multiple transaction dicts with ``parse_transaction``.

    :param data: list of transaction dicts
    :type data: list
    :returns: parsed list of transactions
    :rtype: list
    """

    return [parse_transaction(transaction) for transaction in data]

def parse_ad(ad):
    """
    Parses relevant fields from ad data.

    :param ad: data for one ad
    :type ad: dict
    :returns: parsed ad data
    :rtype: dict
    """

    return {
        'uuid': ad['uuid'],
        'trading_type': ad['trading_type']['action_name'],
        'trading_type_id': ad['trading_type']['id'],
        'payment_method': ad['payment_method']['name'],
        'payment_method_id': ad['payment_method']['id'],
        'coin_currency': ad['coin_currency']['title'],
        'coin_currency_symbol': ad['coin_currency']['symbol'],
        'fiat_currency': ad['fiat_currency']['title'],
        'fiat_currency_symbol': ad['fiat_currency']['symbol'],
        'current_price': float(ad['current_price']),
        'price_formula': ad['price_formula']['display_formula'],
        'price_formula_type': ad['price_formula']['pricing_type'],
        'photo_id_required': ad['photo_id_required'],
        'sms_required': ad['sms_required'],
        'only_friends': ad['only_friends'],
        'trading_hours': ad['trading_hours'],
        'trading_hours_localized': ad['trading_hours_localised'],
        'is_active': ad['is_active'],
        'is_available': ad['is_available'],
        'minimum_feedback': ad['minimum_feedback'],
        'automatic_cancel_time': ad['automatic_cancel_time'],
        'liquidity_tracking': ad['liqudity_tracking'],
        'location_name': ad['location_name'],
        'country_code': ad['country_code'],
        'trading_conditions': ad['trading_conditions'],
        'enforced_sizes': ad['enforced_sizes'],
        'min_trade_size': float(ad['min_trade_size']),
        'max_trade_size': float(ad['max_trade_size']),
        'min_fiat_limit': float(ad['min_fiat_limit']),
        'max_fiat_limit': float(ad['max_fiat_limit']),
        'created_by_username': ad['created_by']['username'],
        'created_by_status': ad['created_by']['activity_status'],
        'created_by_response_time': ad['created_by']['avg_response_time'],
        'created_by_languages': ad['created_by']['languages'],
        'created_by_ratings': ad['created_by']['ratings'],
        'created_by_ratings_percentage': ad['created_by']['ratings_percentage']
    }

def parse_ads(data):
    """
    Parses multiple ads with ``parse_ad``

    :param data: list of ads
    :type data: list
    :returns: list of parsed ads
    :rtype: list
    """

    return [parse_ad(ad) for ad in data]

def parse_trade(trade):
    """
    Parses relevant fields from trade data

    :param trade: data for one trade
    :type trade: dict
    :returns: parsed trade data
    :rtype: dict
    """

    return {
        'id': trade['id'],
        'status': trade['status'],
        'uuid': trade['uuid'],
        'responder': trade['contract_responder']['username'],
        'fiat_amount': float(trade['fiat_amount']),
        'coin_amount': float(trade['coin_amount']),
        'coin_currency': trade['ad']['coin_currency']['title'],
        'coin_currency_symbol': trade['ad']['coin_currency']['symbol'],
        'country_code': trade['ad']['country_code'],
        'location_name': trade['ad']['location_name'],
        'created_by': trade['ad']['created_by']['username'],
        'fiat_currency': trade['fiat_currency']['title'],
        'fiat_currency_symbol': trade['fiat_currency']['symbol'],
        'payment_method': trade['ad']['payment_method']['name'],
        'time_of_expiry': trade['time_of_expiry'],
        'ad_uuid': trade['ad']['uuid']
    }
def parse_trades(data):
    """
    Parses multiple trade dicts with ``parse_trade``

    :param data: list of trades
    :type data: list
    :returns: list of parsed trades
    :rtype: list
    """

    return [parse_trade(trade) for trade in data]

def parse_start_trade(trade):
    """
    Parses return of successful ``start_trade`` request (new trade on an ad)

    :param trade: data for started trade
    :type trade: dict
    :returns: parsed data for started trade
    :rtype: dict
    """

    return {
        'ad_uuid': trade['ad']['uuid'],
        'coin_amount': trade['coin_amount'],
        'coin_currency': trade['coin_currency']['title'],
        'coin_currency_symbol': trade['coin_currency']['symbol'],
        'fiat_amount': trade['fiat_amount'],
        'fiat_currency': trade['fiat_currency']['title'],
        'fiat_currency_symbol': trade['fiat_currency']['symbol'],
        'promo_code': trade['promo_code'],
        'status': trade['status'],
        'time_of_expiry': trade['time_of_expiry'],
        'uuid': trade['uuid'],
    }

def parse_trade_params(data): 
    """
    Parses trade params for use in util functions
    (get_currency_id, get_trade_type, etc.). Used on client initialization.

    :param dict data: api response with trade data
    :returns: parsed params for trades
    :rtype: dict
    """

    def parse_keys(data, *keys):
        return [{key: value[key] for key in keys} for value in data]

    result = {}
    # get id, name and action name for trade types
    result['trade_types'] = parse_keys(data['trade_types'],
                                       'id', 'name', 'action_name')

    # get only id and name for payment methods
    result['payment_methods'] = parse_keys(data['payment_methods'],
                                           'id', 'name')

    # get id, title and symbol for crypto currencies
    result['crypto_currencies'] = parse_keys(data['crypto_currencies'],
                                             'id', 'title', 'symbol')

    # get id, title and symbol for fiat currencies
    result['fiat_currencies'] = parse_keys(data['fiat_currencies'],
                                           'id', 'title', 'symbol')
    return result
