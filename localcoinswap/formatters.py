'''
Pretty prints API data that parsers return.

'''

def print_wallet(data, columns=[], header=True):
    """
    Prints wallet information.

    Available column names (keys):

    - Name (name)
    - Symbol (symbol)
    - ID (id)
    - Coin amount (coin_amount)
    - Fiat amount (fiat_amount), contains amount and currency
    - Address (address)
    - Payment ID (payment_id)

    :param list data: parsed wallet list (return from ``parse_wallet`` 
                      or ``get_wallet``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :returns: None
    """

    data_fields = {
        'name': 'Name',
        'symbol': 'Symbol',
        'id': 'ID',
        'coin_amount': 'Coin amount',
        'fiat_amount': 'Fiat amount',
        'fiat_currency': '',
        'address': 'Address',
        'payment_id': 'Payment ID'
    }
    default_columns = [
        'name',
        'symbol',
        'id',
        'coin_amount',
        'fiat_amount',
        'address',
        'payment_id'
    ]
    columns = validate_columns(columns, data_fields, default_columns)
    if not columns:
        return

    width = get_max_width(data, data_fields)
    # combined width for fiat (amount + currency name)
    width['fiat_amount'] += width['fiat_currency'] + 1

    if header:
        print_header(columns, width, data_fields)

    for wallet in data:
        if 'error' in wallet:
            print(wallet)

        wallet['fiat_amount'] = '{} {}'.format(wallet['fiat_amount'], wallet['fiat_currency'])
        wallet['payment_id'] = wallet['payment_id'] if wallet['payment_id'] else ''
        line = [{c: wallet[c]} for c in columns]
        print(line_formatter(line, width))

def print_deposit_address(data, columns=[], header=True):
    """
    Prints deposit address information.

    Available columns names (keys):

    - Name (name)
    - Symbol (symbol)
    - Balance (balance)
    - Address (address)
    - Payment ID (payment_id)

    :param list data: parsed list of deposit address data (return from 
                      ``parse_deposit_address`` or ``get_deposit_address``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :returns: None
    """

    data_fields = {
        'name': 'Name',
        'symbol': 'Symbol',
        'balance': 'Balance',
        'address': 'Address',
        'payment_id': 'Payment ID'
    }
    default_columns = ['name', 'symbol', 'balance', 'address', 'payment_id']
    columns = validate_columns(columns, data_fields, default_columns)
    if not columns:
        return

    width = get_max_width(data, data_fields)

    if header:
        print_header(columns, width, data_fields)

    for wallet in data:
        if 'error' in wallet:
            print(error)

        wallet['payment_id'] = wallet['payment_id'] if wallet['payment_id'] else ''
        line = [{c: wallet[c]} for c in columns]
        print(line_formatter(line, width))

def print_transactions(data, columns=[], header=True):
    """
    Prints transactions.

    Available column names (keys):

    - Transaction type (transaction_type)
    - From (from)
    - To (to)
    - Amount (amount)
    - Currency (currency)
    - Timestamp (timestamp)

    :param list data: parsed transactions list (return from 
                      ``parse_transactions`` or ``get_transactions``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :returns: None
    """

    if data['count'] == 0:
        print('No transactions found.')
        return

    data_fields  ={
        'transaction_type': 'Transaction type',
        'from': 'From',
        'to': 'To',
        'amount': 'Amount',
        'currency': 'Currency',
        'timestamp': 'Timestamp'
    }
    default_columns = [
        'transaction_type',
        'from',
        'to',
        'amount',
        'currency',
        'timestamp'
    ]
    columns = validate_columns(columns, data_fields, default_columns)
    if not columns:
        return

    width = get_max_width(data['results'], data_fields)

    if len(data['results']) == data['count']:
        print('Found {} transactions:'.format(data['count']))
    else:
        print('Found {} transactions (showing last {}):'.format(data['count'], len(data['results'])))

    if header:
        print_header(columns, width, data_fields)

    for transaction in data['results']:
        if 'error' in transaction:
            print(transaction)

        line = [{c: transaction[c]} for c in columns]
        print(line_formatter(line, width))

# common function for `print_ads` and `print_my_ads`
def print_ads_common(type, data, columns, header=True, summary=True):
    if data['count'] == 0:
        print('No ads found')
        return

    data_fields = {
        'trading_type': 'Trade type',
        'coin_currency': 'Currency',
        'payment_method': 'Payment method',
        'min_trade_size': '',
        'max_trade_size': '',
        'min_fiat_limit': '',
        'max_fiat_limit': '',
        'current_price': 'Current price',
        'coin_currency_symbol': '',
        'fiat_currency_symbol': '',
        'country_code': '',
        'location_name': '',
        'uuid': 'UUID',
        'created_by_username': 'Created by',
        'created_by_response_time': 'Response time',
        'is_active': 'Status',
        'liquidity_tracking': 'Liquidity tracking',
    }
    default_columns = [
        'trading_type',
        'coin_currency',
        'payment_method',
        'limits',
        'current_price',
        'location'
    ]
    if type == 'any':
        default_columns.extend([
            'response_time',
            'uuid'
        ])
    elif type == 'my':
        default_columns.extend([
            'liquidity_tracking',
            'is_active',
            'uuid'
        ])

    width = get_max_width(data['results'], data_fields)

    # add response time for columns
    data_fields['response_time'] = 'Response time'
    width['response_time'] = width['created_by_response_time']
    # combined width for limits
    data_fields['limits'] = 'Limits'
    width['limits'] = max(width['min_trade_size'], width['min_fiat_limit']) \
                      + max(width['max_trade_size'], width['max_fiat_limit']) \
                      + width['fiat_currency_symbol'] + 4
    # combined width for price
    width['current_price'] = width['current_price'] \
                             + width['coin_currency_symbol'] \
                             + width['fiat_currency_symbol'] \
                             + 2
    # combined width for location
    data_fields['location'] = 'Location'
    width['location'] = max(width['country_code'] + width['location_name'] + 2, len(data_fields['location']))

    columns = validate_columns(columns, data_fields, default_columns)
    if not columns:
        return

    if summary:
        if len(data['results']) == data['count']:
            print('Found {} ad{}:'.format(data['count'], 's' * (data['count'] > 1)))
        else:
            print('Found {} ads (showing top {}):'.format(data['count'], len(data['results'])))

    if header:
        print_header(columns, width, data_fields)

    for ad in data['results']:
        if 'error' in ad:
            print(ad)

        # combine min & max limits and currency
        if ad['trading_type_id'] == 1:
            ad['limits'] = '{} - {} {}'.format(ad['min_trade_size'],
                                               ad['max_trade_size'],
                                               ad['fiat_currency_symbol'])
        else:
            ad['limits'] = '{} - {} {}'.format(ad['min_fiat_limit'],
                                               ad['max_fiat_limit'],
                                               ad['fiat_currency_symbol'])
        # combine location name and country
        ad['location'] = '{}, {}'.format(ad['location_name'], ad['country_code'])
        # combine current price and currency
        ad['current_price'] = '{} {}/{}'.format(ad['current_price'],
                                                ad['fiat_currency_symbol'],
                                                ad['coin_currency_symbol'])
        # set response_time
        ad['response_time'] = ad['created_by_response_time']
        # set tracking and status
        ad['liquidity_tracking'] = 'on' if ad['liquidity_tracking'] else 'off'
        ad['is_active'] = 'active' if ad['is_active'] else 'paused'

        # print trading hours (localized or not)?
        line = [{c: ad[c]} for c in columns]
        print(line_formatter(line, width))

def print_ads(data, columns=[], header=True, summary=True):
    """
    Prints ads.

    Available column names (keys):

    - Trade type (trading_type)
    - Currency (coin_currency)
    - Payment method (payment_method)
    - Limits (limits)
    - Current price (current_price)
    - Location (location)
    - Response time (response_time)
    - UUID (uuid)

    :param list data: parsed ads list (return from ``parse_ads`` or ``get_ads``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :param bool summary: print summary ('Found xxx ads...)
    :returns: None
    """

    return print_ads_common('any', data, columns, header, summary)

def print_ad(ad, columns=[], header=True):
    """
    Prints one ad (same format as ``print_ads``).

    :param dict ad: parsed ad (return from ``parse_ad`` or ``get_ad``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :returns: None
    """

    return print_ads({'results': [ad], 'count': 1}, columns, header, summary=False)

def print_my_ads(data, columns=[], header=True, summary=True):
    """
    Prints my ads.

    Available column names (keys):

    - Trade type (trading_type)
    - Currency (coin_currency)
    - Payment method (payment_method)
    - Limits (limits)
    - Current price (current_price)
    - Location (location)
    - Liquidity tracking (liquidity_tracking)
    - Status (is_active)
    - UUID (uuid)

    :param list data: parsed ads list (return from ``parse_ads`` or ``get_my_ads``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :param bool summary: print summary ('Found xxx ads...)
    :returns: None
    """

    return print_ads_common('my', data, columns, header, summary)

def print_my_ad(ad, columns=[], header=True):
    """
    Prints one ad (same format as ``print_my_ads``).

    :param list ad: parsed ad (return from ``parse_ad`` or ``get_my_ad``)
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :returns: None
    """

    return print_my_ads({'results': [ad], 'count': 1}, columns, header, summary=False)

def print_trades(data, columns=[], header=True, summary=True):
    """
    Prints trades.

    Available column names (keys):

    - Status (status)
    - Coin amount (coin_amount)
    - Fiat amount (fiat_amount)
    - Payment method (payment_method)
    - Responder (responder)
    - Created by (created_by)
    - Location (location)
    - Expires (time_of_expiry)
    - Trade UUID (uuid)
    - Ad UUID (ad_uuid)

    :param list data: parsed wallet list (return from 
                      ``parse_trades`` or ``get_trades``).
    :param list columns: list of column names (str) to print (default all)
    :param bool header: print header (default True)
    :param bool summary: print summary ('Found xxx trades...)
    :returns: None
    """

    if data['count'] == 0:
        print('No trades found')
        return

    data_fields = {
        'status': 'Status',
        'coin_currency_symbol': '',
        'fiat_currency_symbol': '',
        'coin_amount': '',
        'fiat_amount': '',
        'payment_method': 'Payment method',
        'responder': 'Responder',
        'created_by': 'Ad created by',
        'country_code': '',
        'location_name': '',
        'time_of_expiry': 'Expires',
        'uuid': 'Trade UUID',
        'ad_uuid': 'Ad UUID'
    }
    default_columns = [
        'status',
        'coin_amount',
        'fiat_amount',
        'payment_method',
        'responder',
        'created_by',
        'location',
        'time_of_expiry',
        'uuid',
        'ad_uuid'
    ]

    width = get_max_width(data['results'], data_fields)

    # combined width for coin amount
    data_fields['coin_amount'] = 'Coin amount'
    width['coin_amount'] = max(width['coin_currency_symbol'] + width['coin_amount'] + 1, len(data_fields['coin_amount']))
    # combined width for fiat amount
    data_fields['fiat_amount'] = 'Fiat amount'
    width['fiat_amount'] = max(width['fiat_currency_symbol'] + width['fiat_amount'] + 1, len(data_fields['fiat_amount']))
    # combined width for location
    data_fields['location'] = 'Location'
    width['location'] = max(width['country_code'] + width['location_name'] + 2, len(data_fields['location']))

    columns = validate_columns(columns, data_fields, default_columns)
    if not columns:
        return

    if summary:
        if len(data['results']) == data['count']:
            print('Found {} trade{}:'.format(data['count'], 's' * (data['count'] > 1)))
        else:
            print('Found {} trades (showing top {}):'.format(data['count'], len(data['results'])))

    if header:
        print_header(columns, width, data_fields)

    for trade in data['results']:
        if 'error' in trade:
            print(trade)

        # combine amounts and currencies
        trade['coin_amount'] = '{} {}'.format(trade['coin_amount'],
                                              trade['coin_currency_symbol'])
        trade['fiat_amount'] = '{} {}'.format(trade['fiat_amount'],
                                              trade['fiat_currency_symbol'])
        # combine location name and country
        trade['location'] = '{}, {}'.format(trade['location_name'],
                                            trade['country_code'])

        line = [{c: trade[c]} for c in columns]
        print(line_formatter(line, width))

def print_trade(trade, columns=[]):
    """
    Prints one trade (same format as ``print_trades``).

    :param dict trade: parsed trade (return from ``parse_trade`` or ``get_trade``).
    :returns: None
    """

    return print_trades({'results': [trade], 'count': 1}, columns, summary=False)

# Returns a set of columns that are present in fields (key or value),
# prints invalid columns
def validate_columns(columns, fields, default):
    def find_in_values(column, fields):
        for k, v in fields.items():
            if column.lower() == k or column.lower() == v.lower():
                return k

    if not columns:
        return default

    valid, invalid = [], []

    for c in columns:
        _column = find_in_values(c, fields)
        if _column:
            valid.append(_column)
        else:
            invalid.append(c)
    if invalid:
        print('Invalid columns: {}'.format(', '.join(invalid)))
    return valid

# Returns line columns formatted with width
def line_formatter(line, width):
    return ' | '.join(['{: <{w}}'.format(column[key], w = width[key]) for column in line for key in column])

# Print column names and separator line
def print_header(columns, width, data_fields):
    header = [{c: data_fields[c]} for c in columns]
    print(line_formatter(header, width))
    print('-+-'.join(['-' * width[c] for c in columns]))

# Helper function for prints, goes over dicts in data and 
# calculates max width of each column.
def get_max_width(data, columns):
    return {
        key: max(max([len(str(d[key])) for d in data]), len(name)) for key, name in columns.items()
    }
