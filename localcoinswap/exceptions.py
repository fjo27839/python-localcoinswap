class LocalcoinswapAPIException(Exception):
    """
    API Exception (non-2xx responses).

    Attributes:

    - error: API error response message (json or string)
    - response: response object
    - request: request object (if available)

    """

    def __init__(self, response):
        try:
            self.error = response.json()
        except ValueError:
            message = response.text
            if len(message) > 100:
                message = '{}...(truncated)'.format(message[:99])
            self.error = '(non-json response) {}'.format(message)
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'API error: ({} {}) {}'.format(self.response.status_code,
                                              self.response.reason,
                                              self.error)

class LocalcoinswapResponseException(Exception):
    """
    Response Exception (non-json response when json was expected).
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

class LocalcoinswapInvalidParamError(Exception):
    """
    Utils Exception (tried to use invalid currency, payment method, etc.)
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
