Client
======

Create API client and retrieve your deposit information for BTC wallet:

.. code-block:: text

	In [1]: from localcoinswap.client import Client
	In [2]: from pprint import pprint

	In [3]: client = Client('my_api_token')

	In [4]: client.get_deposit_address('btc')
	Out[4]: [{'name': 'Bitcoin', 'symbol': 'BTC', 'balance': 12.345, 'address': '1HqgJweqgDKQ2Xxxxxxxxxxxxxxxxxxxxx', 'payment_id': None}]

Wallet
------

Print your portfolio (all currencies, print only name, address and payment id):

.. code-block:: text

	IN [1]: from localcoinswap.formatters import print_wallet

	In [2]: print_wallet(client.get_wallet(), ['name', 'address', 'payment id'])
	Out[2]:
	Name     | Address                                    | Payment ID
	---------+--------------------------------------------+-----------
	Bitcoin  | 1HqgJwxxxxxxxxxxxxxxxxxxxxxxxxxxxx         |
	Ethereum | 0xd64d35xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx |
	XRP      | rsRhmFHxxxxxxxxxxxxxxxxxxxxxxxxxxx         | 101010
	...

Get deposit addresses for BTC and Ethereum:

.. code-block:: text

	In [1]: client.get_deposit_address(['btc', 'Ethereum'])
	Out[1]:
	[{'address': '1HqgJwxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	  'balance': 0.0,
	  'name': 'Bitcoin',
	  'payment_id': None,
	  'symbol': 'BTC'},
	 {'address': '0xd64d35xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	  'balance': 0.009898,
	  'name': 'Ethereum',
	  'payment_id': None,
	  'symbol': 'ETH'}]

Get last 3 transactions:

.. code-block:: text

	In [1]: client.get_transactions(limit=3)
	Out[1]:
	{'count': 8,
	 'limit': 3,
	 'results': [{'amount': '-0.500000000000000000',
	              'currency': 'ETH',
	              'from': 'user',
	              'timestamp': 1557336630,
	              'to': '0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	              'transaction_type': 'contract_escrow_release'},
	             {'amount': '-0.500000000000000000',
	              'currency': 'ETH',
	              'from': 'user',
	              'timestamp': 1557336630,
	              'to': 'escrow',
	              'transaction_type': 'contract_escrow'},
	             {'amount': '-0.000001000000000000',
	              'currency': 'ETH',
	              'from': 'user',
	              'timestamp': 1557336535,
	              'to': '0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
	              'transaction_type': 'contract_fees'}],
	 'total_pages': 3}

Print all your transactions:

.. code-block:: text

	In [1]: from localcoinswap.formatters import print_transactions

	In [2]: print_transansactions(client.get_transactions(get_all=True))
	Out[2]:
	Found 8 transactions:
	Transaction type        | From   | To                                         | Amount                | Currency | Timestamp
	------------------------+--------+--------------------------------------------+-----------------------+----------+-----------
	contract fees           | user   | 0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | -0.000100000000000000 | ETH      | 1557336630
	contract escrow         | user   | escrow                                     | -0.010000000000000000 | ETH      | 1557336630
	contract fees           | user   | 0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | -0.000001000000000000 | ETH      | 1557336535
	contract escrow release | escrow | user                                       | 0.000100000000000000  | ETH      | 1557336535
	contract fees           | user   | 0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | -0.000001000000000000 | ETH      | 1557336269
	contract escrow release | escrow | user                                       | 0.000100000000000000  | ETH      | 1557336268
	contract fees           | user   | 0x15e13Exxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | -0.000200000000000000 | ETH      | 1555611541
	contract escrow release | escrow | user                                       | 0.020000000000000000  | ETH      | 1555611541

Create a withdrawal (input OTP manually):

.. code-block:: text

	In [1]: otp = input('OTP: ')
	Out[1]: OTP: xxxxxx

	In [2]: client.withdraw('ETH', 'destination_address', 1.5, otp)
	Out[2]: {'id': 123}

Advertisements
--------------

Get and print all of your active advertisements:

.. code-block:: text

	In [1]: from localcoinswap.formatters import print_my_ads

	In [2]: print_my_ads(client.get_my_ads('active', get_all=True))
	Out[2]:
	Found 1 ad:
	Trade type | Currency | Payment method | Limits          | Current price            | Location      | Liquidity tracking | Status | UUID
	-----------+----------+----------------+-----------------+--------------------------+---------------+--------------------+--------+-------------------------------------
	Buying     | Ethereum | Cash in person | 1.0 - 100.0 JPY | 25774.4004698945 JPY/ETH | Akihabara, JP | off                | active | 3c7a5xxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Pause ad:

.. code-block:: text

	In [1]: client.pause_ad('my_ad_uuid')
	Out[1]: {'uuid': 'my_ad_uuid', 'is_active': False, 'is_available': True}

Resume ad:

.. code-block:: text

	In [1]: client.resume_ad('my_ad_uuid')
	Out[1]: {'uuid': 'my_ad_uuid', 'is_active': True, 'is_available': True}

Delete ad:

.. code-block:: text

	In [1]: client.delete_ad('my_ad_uuid')
	Out[1]: {'deleted': 'my_ad_uuid'}

Print a list of 5 open advertisements (Buying ETH, Worlwide; print only
payment method, limits, location, current price and ad uuid):

.. code-block:: text

	In [1]: from localcoinswap.formatters import print_ads

	In [2]: print_ads(client.get_ads({'limit': 5, 'coin_currency': 2, 'trading_type': 1}))
	Out[2]:
	Found 5 ads:
	Payment method      | Limits            | Location      | Current price            | UUID
	--------------------+-------------------+---------------+--------------------------+-------------------------------------
	Cash Deposit        | 25.0 - 500.0 AUD  | Sydney, AU    | 341.0888100134 AUD/ETH   | a0b2456a-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	Cash Deposit        | 200.0 - 500.0 CNY | Moscow, RU    | 1474.8460435364 CNY/ETH  | 17eaec08-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	Local Bank transfer | 1.0 - 100.0 AUD   | Barcelona, ES | 341.0888100134 AUD/ETH   | 887d6955-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	Cash in person      | 1.0 - 100.0 JPY   | Akihabara, JP | 25799.8390013759 JPY/ETH | 3c7a590a-xxxx-xxxx-xxxx-xxxxxxxxxxxx
	Abra                | 1.0 - 10.0 AFN    | Quito, EC     | 18901.9026800881 AFN/ETH | c19801cc-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Get information on a specific ad:

.. code-block:: text

	In [1]: client.get_ad('c19801cc-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
	Out[1]:
	{'automatic_cancel_time': '120',
	 'coin_currency': 'Ethereum',
	 'coin_currency_symbol': 'ETH',
	 'country_code': 'EC',
	 'created_by_languages': [],
	 'created_by_ratings': None,
	 'created_by_ratings_percentage': None,
	 'created_by_response_time': 0,
	 'created_by_status': 'active',
	 'created_by_username': 'user3',
	 'current_price': 18917.8082843877,
	 'enforced_sizes': '',
	 'fiat_currency': 'Afghan Afghani',
	 'fiat_currency_symbol': 'AFN',
	 'is_active': True,
	 'is_available': True,
	 'liquidity_tracking': False,
	 'location_name': 'Quito',
	 'max_fiat_limit': 10.0,
	 'max_trade_size': 10.0,
	 'min_fiat_limit': 1.0,
	 'min_trade_size': 1.0,
	 'minimum_feedback': '0',
	 'only_friends': False,
	 'payment_method': 'Abra',
	 'payment_method_id': 43,
	 'photo_id_required': False,
	 'price_formula': '-1',
	 'price_formula_type': 'MARGIN',
	 'sms_required': False,
	 'trading_conditions': '',
	 'trading_hours': 'Mon - Sun: Trading all day<br />',
	 'trading_hours_localized': 'Mon - Sun: Trading all day<br />',
	 'trading_type': 'Buying',
	 'trading_type_id': 1,
	 'uuid': 'c19801cc-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

Trades
------

Get and print a short list of your active trades (limit of 10):

.. code-block:: text

	In [1]: from localcoinswap.formatters import print_trades

	In [2]: print_trades(client.get_active_trades()) # `get_inactive_trades` & `get_all_trades` are also available
	Out[2]:
	Found 1 trade:
	Status     | Coin amount      | Fiat amount | Payment method | Responder | Ad created by | Location      | Expires    | Trade UUID                           | Ad UUID
	-----------+------------------+-------------+----------------+-----------+---------------+---------------+------------+--------------------------------------+-------------------------------------
	CRYPTO_ESC | 0.0005802757 ETH | 15.0 JPY    | Cash in person | user 1	 | my_user	     | Akihabara, JP | 1558622115 | b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx | 3c7a590a-xxxx-xxxx-xxxx-xxxxxxxxxxxx

Get information on a specific trade:

.. code-block:: text

	In [1]: client.get_trade('b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
	Out[1]:
	{'ad_uuid': '3c7a590a-xxxx-xxxx-xxxx-xxxxxxxxxxxx',
	 'coin_amount': 0.0005802757,
	 'coin_currency': 'Ethereum',
	 'coin_currency_symbol': 'ETH',
	 'country_code': 'JP',
	 'created_by': 'my_user',
	 'fiat_amount': 15.0,
	 'fiat_currency': 'Japanese Yen',
	 'fiat_currency_symbol': 'JPY',
	 'id': 187,
	 'location_name': 'Akihabara',
	 'payment_method': 'Cash in person',
	 'responder': 'user1',
	 'status': 'CRYPTO_ESC',
	 'time_of_expiry': 1558622115,
	 'uuid': 'b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

Reject trade:

.. code-block:: text

	In [1]: client.reject_trade('b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
	Out[1]: {'status': 'REJECTED', 'uuid': 'b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

Accept trade:

.. code-block:: text

	In [1]: client.accept_trade('b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
	Out[1]: {'status': 'ACCEPTED', 'uuid': 'b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

Respond to trade that you have paid to the other party:

.. code-block:: text

	In [1]: client.paid_trade('b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx')
	Out[1]: {'status': 'FUND_PAID', 'uuid': 'b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

Confirm transfer and finish the trade (requires OTP):

.. code-block:: text

	In [1]: otp = input('OTP: ')
	Out[1]: OTP: 123456

	In [2]: client.confirm_trade('b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx', otp)
	Out[2]: {'status': 'COMPLETED', 'uuid': 'b81ae9a0-xxxx-xxxx-xxxx-xxxxxxxxxxxx'}

API reference
-------------

.. automodule:: localcoinswap.client
  :members:

