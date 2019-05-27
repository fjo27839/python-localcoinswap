Python module for LocalCoinSwap
===============================

Welcome to the documentation for the ``localcoinswap`` Python module.

This module provides a set of tools for interacting with LocalCoinSwap APIs in Python.

Project homepage: https://github.com/LocalCoinSwap/python-localcoinswap

:Version: |version|

Quick Start
-----------

1. `Register an account with LocalCoinSwap <https://localcoinswap.com/en/register>`_

2. Generate API token (Settings -> APIs)

3. Clone and install `python-localcoinswap` from GitHub:

.. code-block:: bash

	git clone https://github.com/LocalCoinSwap/python-localcoinswap.git
	cd python-localcoinswap
	# create and enable virtualenv (optional)
	virtualenv -p python3 venv
	source venv/bin/activate
	# install requirements
	pip install -r requirements.txt
	python setup.py install

4. Start using this library:

.. code-block:: python

	from localcoinswap.client import Client
	from localcoinswap.formatters import print_deposit_address, print_ads
	from localcoinswap.utils import get_currency_id

	# Setup api client
	client = Client("my_api_token")

	# Get all wallets
	wallet = client.get_wallet()

	# Get and print deposit information for Bitcoin
	print_deposit_address(client.get_deposit_address('BTC'))

	# Get top 10 ads (buy or sell) for Ethereum sorted by popularity
	#  prepare filters:
	filters = {
	    'limit': 10,
	    'coin_currency': get_currency_id(client.trade_params, 'Ethereum'),
	    'ordering': '-popularity'
	}
	#  get parsed ad data
	ads = client.get_ads(filters)
	#  print ads (optional)
	print_ads(ads)	

.. toctree::
   :maxdepth: 2
   :hidden:
   :glob:

   *

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
