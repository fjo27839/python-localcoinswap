import requests

from .utils import (get_crypto_currency_id,
                    get_fiat_currency_id,
                    get_payment_method_id,
                    get_trade_type_id)
from .parsers import (parse_ad,
                      parse_ads,
                      parse_deposit_address,
                      parse_start_trade,
                      parse_trade,
                      parse_trades,
                      parse_trade_params,
                      parse_transactions,
                      parse_wallet)
from .exceptions import (LocalcoinswapAPIException,
                         LocalcoinswapResponseException)

class Client:
    """
    LCS API client.

    Provides a set of methods to interact with various APIs (wallet, ads, trades, etc.).

    Attributes:

    - base_url (str): base url for other methods
    - trade_params (dict): various trade parameterss (available currencies, trade types, etc.) 
      that are used in utils functions to convert user input to validated formats
      if necessary (e.g. crypto currency symbol to id)

    :param str token: api auth token
    :param bool get_params: get trade data parameters on startup (default True)
    """

    API_URL = 'https://api.localcoinswap.com'

    def __init__(self, token, get_params=True):
        self.token = token
        # hardcoding locale for now
        self.base_url = '{}/en/api'.format(self.API_URL)
        self.session = self.create_session()
        if get_params:
            self.set_trade_params()

    def create_session(self):
        session = requests.session()
        session.headers.update({
            'User-Agent': 'localcoinswap/python',
            'Authorization': 'Token {}'.format(self.token)
        })
        return session

    def create_api_url(self, path):
        return '{}/{}'.format(self.base_url, path)

    # Internal function for handling requests in a session
    def request(self, method, url, data={}, timeout=10, non_json_response=False):
        response = getattr(self.session, method)(url,
                                                 data=data,
                                                 timeout=timeout)

        return self.handle_response(response, non_json_response)

    # Request paginated data from api (used in various get_ methods in Client).
    # returns additional data if request is for first page (count & total pages)
    def request_page(self, url, timeout=10, first=False):
        response = self.request('get', url, timeout=timeout)
        if first:
            return (response['results'],
                    response['next'],
                    response['count'],
                    response['total_pages'])
        return response['results'], response['next']

    # Handle response (status code, json decoding, etc.)
    def handle_response(self, response, non_json_response=False):
        if response.status_code not in [200, 201, 204]:
            raise LocalcoinswapAPIException(response)
        if non_json_response:
            return response.text
        try:
            return response.json()
        except ValueError:
            raise LocalcoinswapResponseException('Response is not json: {}'.format(response.text))

    def get_trade_params(self):
        """
        Retrieve and parse available trade parameters
        (currencies, trade types, payment methods, etc.)

        :returns: dictionary of parsed trade params
        :rtype: dict

        .. code-block:: python

            {
                'currencies': [
                    {'id': 1, 'symbol': 'BTC', 'title': 'Bitcoin'},
                    ...
                    {'id': 10001, 'symbol': 'USD', 'title': 'United States Dollar'},
                    ...
                ],
                'payment_methods': [
                    {'id': 1, 'name': 'Local Bank transfer'},
                    {'id': 2, 'name': 'Cash Deposit'},
                    {'id': 3, 'name': 'Cash in person'},
                    ...
                ],
                'trade_types': [
                    {'action_name': 'Buying', 'id': 1, 'name': 'buy'},
                    {'action_name': 'Selling', 'id': 2, 'name': 'sell'}
                ]
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return parse_trade_params(self.request('get', self.create_api_url('new-trade/')))

    def set_trade_params(self):
        """
        Retrieve and set self.trade_parameters (see ``get_trade_params``).

        :returns: None

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        self.trade_params = self.get_trade_params()

    '''
    Wallet operations (portfolio, deposit addresses, withdrawal, transactions)
    '''

    def get_wallet(self, raw=False):
        """
        Retrieves wallet data (all addresses/currencies and their balance).

        :param bool raw: return raw reponse from api (default False)
        :returns: list of dicts with address data for each currency
        :rtype: list

        .. code-block:: python

            # parsed response:
            [
                {
                    'address': '1525DXxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    'coin_amount': 0.04321,
                    'fiat_amount': 352.322321230272,
                    'fiat_currency': 'USD',
                    'id': 1,
                    'name': 'Bitcoin',
                    'payment_id': None,
                    'symbol': 'BTC'
                },
                ...
                {
                    'address': 'rsRhmFHxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    'coin_amount': 0.0,
                    'fiat_amount': 0.0,
                    'fiat_currency': 'USD',
                    'id': 17,
                    'name': 'XRP',
                    'payment_id': '1234567890',
                    'symbol': 'XRP'
                }
            ]

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return get_result(raw,
                          self.request(
                            'get',
                            self.create_api_url('wallet/AJAX/get-portfolio-data/')),
                          parse_wallet)

    def get_deposit_address(self, currencies, raw=False):
        """
        Retrieves deposit information for selected currency/currencies.

        :param str/list currencies: name or list of currency names
        :param bool raw: return raw reponse from api (default False)
        :returns: list of dicts with address data for each currency
        :rtype: list

        .. code-block:: python

            # parsed response:
            [
                {
                    'address': '0xfD6724xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                    'balance': 0.0123,
                    'name': 'Ethereum',
                    'payment_id': None,
                    'symbol': 'ETH'
                }
            ]

        :raises: LocalcoinswapAPIException,
                 LocalcoinswapResponseException,
                 LocalcoinswapInvalidParamError

        """

        if type(currencies) is not list:
            currencies = [currencies]
        result = []

        for currency in currencies:
            result.append(
                get_result(
                    raw,
                    self.request(
                        'get',
                        self.create_api_url('wallet/AJAX/get-wallet-info/{}/'.format(
                            get_crypto_currency_id(self.trade_params, currency))
                        )
                    ),
                    parse_deposit_address
                )
            )
        return result

    def withdraw(self, currency, to_address, amount, otp, pid=None, raw=False):
        """
        Withdraw from your wallet.

        :param int/str currency: currency name, symbol or id
        :param str to_address: destination address
        :param float amount: amount (float, e.g. 1.23 BTC)
        :param int otp: 6-digit OTP code
        :param int pid: payment id / destination tag (e.g. for Ripple)
        :param bool raw: return raw reponse from api (default False)
        :returns: dictionary/json withdraw data or error info
        :rtype: dict

        .. code-block:: python

            # successful withdrawal (parsed response):
            {
                'id': 123
            }

        :raises: LocalcoinswapAPIException,
                 LocalcoinswapResponseException,
                 LocalcoinswapInvalidParamError

        """

        data = {
            'currency': get_crypto_currency_id(self.trade_params, currency),
            'to_address': to_address,
            'amount': amount,
            'otp': otp,
        }
        if pid:
            data.update({'to_chip': pid})

        return get_result(raw,
                          self.request('post',
                                       self.create_api_url('wallet/withdraw/create/'),
                                       data,
                                       timeout=20),
                          lambda r: {'id': r['id']})

    def get_transactions(self, limit=20, get_all=False, timeout=10, raw=False):
        """
        List transactions.

        :param int limit: number of returned transactions (default 20)
        :param bool get_all: retrieve all transactions
                             disregarding limit value (default False)
        :param int timeout: request timeout value for high limit values (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json transactions data or error info
        :rtype: dict

        .. code-block:: python

            # parsed response (get_all=False):
            {
                'count': 8,
                'limit': 20,
                'total_pages': 1,
                'results': [
                    {
                        'amount': '-0.000100000000000000',
                        'currency': 'ETH',
                        'from': 'alex_csrf',
                        'timestamp': 1557336630,
                        'to': '0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
                        'transaction_type': 'contract_fees'
                    },
                    ...
                ]
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        results = []

        current_page, next_page_url, count, total_pages = self.request_page(
            self.create_api_url('wallet/transactions/?limit={}&offset=0'.format(limit)),
            timeout,
            True)
        results += get_result(raw, current_page, parse_transactions)

        if get_all:
            while next_page_url:
                current_page, next_page_url = self.request_page(next_page_url, timeout)
                results += get_result(raw, current_page, parse_transactions)
            return {'count': count, 'results': results}

        return {'count': count,
                'total_pages': total_pages,
                'limit': limit,
                'results': results}

    '''
    Ad operations (list, create, update, pause, resume, delete)
    '''

    def get_ad(self, uuid, raw=False):
        """
        Retrieve data on selected ad.

        :param str uuid: ad uuid
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json data for selected ad
        :rtype: dict

        .. code-block:: python

            # parsed response
            {
                'automatic_cancel_time': '120',
                'coin_currency': 'Ethereum',
                'coin_currency_symbol': 'ETH',
                'country_code': 'ES',
                'created_by_languages': [],
                'created_by_ratings': None,
                'created_by_ratings_percentage': None,
                'created_by_response_time': 507,
                'created_by_status': 'active',
                'created_by_username': 'user1',
                'current_price': 16302.5912738867,
                'enforced_sizes': '',
                'fiat_currency': 'Afghan Afghani',
                'fiat_currency_symbol': 'AFN',
                'is_active': True,
                'is_available': True,
                'liquidity_tracking': False,
                'location_name': 'Toledo',
                'max_fiat_limit': 1000000.0,
                'max_trade_size': 1000000.0,
                'min_fiat_limit': 1.0,
                'min_trade_size': 1.0,
                'minimum_feedback': '0',
                'only_friends': False,
                'payment_method': 'Cash in person',
                'payment_method_id': 3,
                'photo_id_required': False,
                'price_formula': '-1',
                'price_formula_type': 'MARGIN',
                'sms_required': False,
                'trading_conditions': '',
                'trading_hours': 'Mon - Sun: Trading all day<br />',
                'trading_hours_localized': 'Mon - Sun: Trading all day<br />',
                'trading_type': 'Buying',
                'trading_type_id': 1,
                'uuid': 'dc01xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return get_result(raw,
                          self.request('get',
                                       self.create_api_url('trade/{}'.format(uuid))),
                          parse_ad)

    def get_ads(self, params={}, get_all=False, timeout=10, raw=False):
        """
        List ads with optional sorting/filtering parameters.

        Parameters:

        - *limit*: maximum number of returned results (per page)
        - *offset*: (optional) offset for paginated results
                    (when `get_all=False`)
        - *ordering*: see below for ordering parameters

        Filtering parameters (see ``localcoinswap.utils`` for
        available conversion functions):

        - *coin_currency*: crypto currency id
        - *fiat_currency*: fiat_currency id
        - *trading_type*: trading type id
        - *payment_method*: payment method id
        - *location*: location name (e.g. 'London')
        - *country*: country code (e.g. 'ES')

        Ordering parameter values (if values below are prefixed with ``-``
        results will be sorted in descending order):

        - *coin_currency__priority*: order by currency priority
        - *fiat_currency__priority*: order by fiat currency priority
        - *payment_method__name*: order by payment method alphabetically
        - *current_price*: order by price per unit in fiat amount
        - *current_price_usd*: order by price per unit in usd amount
        - *coin_currency__symbol*: order alphabetically by coin symbol
        - *fiat_currency__symbol*: order alphabetically by fiat symbol
        - *popularity*: order by popularity

        Multiple ordering parameters can be used, but must be comma separated,
        e.g: `{'ordering': '-payment_method__name,current_price_usd'}`

        :param dict params: sorting and filtering parameters
                            (default `{'limit': 20, 'ordering': '-popularity'}`)
        :param bool get_all: retrieve all available ads with selected filters
                             (default False)
        :param int timeout: request timeout value for high number
                            of results (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json of ad data
        :rtype: dict

        .. code-block:: python

            # parsed response (get_all=False, all Ethereum ads):
            {
                'count': 6,
                'limit': 20,
                'results': [
                    {ad1}, # see 'get_ad'
                    {ad2},
                    ...
                ],
                'total_pages': 1
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        params.update({
            'limit': params.get('limit', 20),
            'ordering': params.get('ordering', '-popularity')
        })
        prepped_params = '&'.join(['{}={}'.format(param, value) for param, value in params.items()])

        results = []

        current_page, next_page_url, count, total_pages = self.request_page(
            self.create_api_url('trade/?{}'.format(prepped_params)),
            timeout,
            True)
        results += get_result(raw, current_page, parse_ads)

        if get_all:
            while next_page_url:
                current_page, next_page_url = self.request_page(next_page_url, timeout)
                results += get_result(raw, current_page, parse_ads)
            return {'count': count, 'results': results}

        return {'count': count,
                'total_pages': total_pages,
                'limit': params.get('limit', 20),
                'results': results}

    def get_my_ads(self, ad_type='all', limit=5, get_all=False, timeout=10, raw=False):
        """
        Retrieve your ads.

        :param str ad_type: 'active', 'inactive' or 'all' for both types (default 'all')
        :param int limit: max number of ads in result (default 5)
        :param bool get_all: retrieve all available ads of selected type
                             (default False)
        :param int timeout: request timeout value for high number
                            of results (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json ad data (same as ``get_ads``)
        :rtype: dict

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        results = []

        current_page, next_page_url, count, total_pages = self.request_page(
            self.create_api_url('user-trade/{}/?limit={}&offset=0'.format(ad_type, limit)),
            timeout,
            True)
        results += get_result(raw, current_page, parse_ads)

        if get_all:
            while next_page_url:
                current_page, next_page_url = self.request_page(next_page_url, timeout)
                results += get_result(raw, current_page, parse_ads)
            return {'count': count, 'results': results}

        return {'count': count,
                'total_pages': total_pages,
                'limit': limit,
                'results': results}

    # internal method for controlling ads, shouldn't be used directly
    # used by 'pause_ad', 'resume_ad' and 'delete_ad'
    def control_ad(self, op, uuid, raw):
        url = self.create_api_url('user-trade/update-delete/{}/'.format(uuid))

        if op == 'delete':
            # delete doesn't return anything, so using non_json_response
            # to grab response.text (avoid exceptions)
            response = self.request('delete', url, non_json_response=True)
            return {'deleted': uuid}

        data = {'is_active': op == 'resume'}
        return get_result(raw,
                          self.request('patch', url, data),
                          lambda r: {'uuid': r['uuid'],
                                     'is_active': r['is_active'],
                                     'is_available': r['is_available']})

    def pause_ad(self, uuid, raw=False):
        """
        Pause selected ad.

        Raw response can be parsed with ``parsers.parse_ad`` if more data
        is required than default parsed response.

        :param str uuid: selected ad uuid
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json ad data
        :rtype: dict

        .. code-block:: python

            # parsed response:
            {
                'is_active': False,
                'is_available': True,
                'uuid': 'dc01xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.control_ad('pause', uuid, raw)

    def resume_ad(self, uuid, raw=False):
        """
        Resume selected ad.

        Raw response can be parsed with ``parsers.parse_ad`` if more data
        is required than default parsed response.

        :param str uuid: selected ad uuid
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json ad data
        :rtype: dict

        .. code-block:: python

            # parsed response:
            {
                'is_active': True,
                'is_available': True,
                'uuid': 'dc01xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.control_ad('resume', uuid, raw)

    def delete_ad(self, uuid):
        """
        Delete selected ad.

        :param str uuid: selected ad uuid
        :returns: dictionary/json ad data
        :rtype: dict

        .. code-block:: python

            {
                'deleted': 'dc01xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.control_ad('delete', uuid, False)
        
    '''
    Trade (ie contract) operations (list, respond to, ...)
    '''

    def get_trade(self, uuid, raw=False):
        """
        Retrieve selected trade.

        :param str uuid: selected trade uuid
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            # parsed response:
            {
                'ad_uuid': 'dc01xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
                'coin_amount': 0.0001,
                'coin_currency': 'Ethereum',
                'coin_currency_symbol': 'ETH',
                'country_code': 'ES',
                'created_by': 'user1',
                'fiat_amount': 1.3,
                'fiat_currency': 'Afghan Afghani',
                'fiat_currency_symbol': 'AFN',
                'id': 321,
                'location_name': 'Toledo',
                'payment_method': 'Cash in person',
                'responder': 'user2',
                'status': 'REJECTED',
                'time_of_expiry': 1557345712,
                'uuid': '6a83xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return get_result(raw,
                          self.request('get',
                                       self.create_api_url('contracts/{}/'.format(uuid))),
                          parse_trade)

    # Internal function for 'get_all_trades', 'get_active_trades',
    # 'get_inactive_trades'. No reason to use directly
    def get_trades(self, trade_type, limit=10, get_all=False, timeout=10, raw=False):
        results = []

        current_page, next_page_url, count, total_pages = self.request_page(
            self.create_api_url('contracts/{}/?limit={}&offset=0'.format(trade_type, limit)),
            timeout,
            first=True
        )
        results += get_result(raw, current_page, parse_trades)

        if get_all:
            while next_page_url:
                current_page, next_page_url = self.request_page(next_page_url, timeout)
                results += get_result(raw, current_page, parse_trades)
            return {'count': count, 'results': results}

        return {'count': count,
                'total_pages': total_pages,
                'limit': limit,
                'results': results}

    def get_active_trades(self, limit=10, get_all=False, timeout=10, raw=False):
        """
        Retrieve your active trades.

        :param int limit: max number of trades in result or number of trades 
                          per page if get_all=True (default 10)
        :param bool get_all: retrieve all available trades (default False)
        :param int timeout: request timeout value for high limit values (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            # parsed response (get_all=True):
            {
                'count': 3,
                'results': [
                    {trade1}, # see 'get_trade'
                    {trade2},
                    ...
                ]
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.get_trades('active', limit, get_all, timeout, raw)

    def get_inactive_trades(self, limit=10, get_all=False, timeout=10, raw=False):
        """
        Retrieve your inactive trades.

        :param int limit: max number of trades in result or number of trades per page
                          if get_all=True (default 10)
        :param bool get_all: retrieve all available trades (default False)
        :param int timeout: request timeout value for high limit values (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            # parsed response (limit 5):
            {
                'count': 18,
                'limit': 5,
                'total_pages': 4,
                'results': [
                    {trade1}, # see 'get_trade'
                    {trade2},
                    ...
                ]
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.get_trades('inactive', limit, get_all, timeout, raw)

    def get_all_trades(self, limit=10, get_all=False, timeout=10, raw=False):
        """
        Retrieve combined result of active and inactive trades.

        :param int limit: max number of trades (for each type) in result or number
                          of trades per page if get_all=True (default 10)
        :param bool get_all: retrieve all available trades (default False)
        :param int timeout: request timeout value for high limit values (default 10 seconds)
        :param bool raw: return raw reponse from api or parsed data
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            # parsed response (limit 5):
            {
                'count': 19, # sum of active and inactive trades
                'limit': 5,
                'results': [
                    {trade1}, # see 'get_trade'
                    {trade2},
                    ...
                ],
                'total_pages': {
                    'active': 1,
                    'inactive': 4
                }
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        active = self.get_active_trades(limit, get_all, timeout, raw)
        inactive = self.get_inactive_trades(limit, get_all, timeout, raw)

        result = {'count': active['count'] + inactive['count'],
                  'results': active['results'] + inactive['results']}
        if not get_all:
            extra = {'total_pages': {'active': active['total_pages'],
                                     'inactive': inactive['total_pages']},
                     'limit': limit}
            result.update(extra)

        return result

    # Respond to trade. Shouldn't be used directly, use 'accept_trade',
    # 'reject_trade', 'paid_trade' or 'confirm_trade' instead.
    def respond_to_trade(self, uuid, trade_response, otp=None):
        data = {'status': trade_response}
        if otp:
            data.update({'otp': otp})

        return get_result(False,
                          self.request('patch',
                                       self.create_api_url(
                                            'contracts/status/{}/'.format(uuid)),
                                       data),
                          lambda r: {'uuid': uuid, 'status': r['status']})

    def reject_trade(self, uuid):
        """
        Reject open trade.

        :param str uuid: trade uuid
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            {
                'status': 'REJECTED',
                'uuid': '6a83xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.respond_to_trade(uuid, 'REJECTED')

    def accept_trade(self, uuid):
        """
        Accept open trade.

        :param str uuid: trade uuid
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            {
                'status': 'ACCEPTED',
                'uuid': '6a83xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.respond_to_trade(uuid, 'ACCEPTED')

    def paid_trade(self, uuid):
        """
        Respond that funds have been paid to the other party.

        :param str uuid: trade uuid
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            {
                'status': 'FUND_PAID',
                'uuid': '6a83xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.respond_to_trade(uuid, 'FUND_PAID')

    def confirm_trade(self, uuid, otp):
        """
        Confirm that funds were received (finish trade).

        :param str uuid: trade uuid
        :param int otp: 6-digit OTP code
        :returns: dictionary/json trade data or error info
        :rtype: dict

        .. code-block:: python

            {
                'status': 'COMPLETED',
                'uuid': '6a83xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
            }

        :raises: LocalcoinswapAPIException, LocalcoinswapResponseException

        """

        return self.respond_to_trade(uuid, 'FUND_RECEIVED', otp)

'''
Helper functions
'''

# selects result return between raw api response and parsed with parser
def get_result(raw, result, parser):
    return result if raw else parser(result)
