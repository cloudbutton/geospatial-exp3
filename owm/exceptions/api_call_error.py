"""
Module containing APICallError class.

AUTHOR: Juanjo

DATE: 08/01/2018

"""

import os

from . import OWMError


class APICallError(OWMError):
    """
    Error class that represents generic failures when invoking OWM web API, for
    example due to network errors.

    :param str message: the message of the error
    :param Exception triggering_error: optional *Exception* object that triggered this
        error (defaults to ``None``)

    """

    def __init__(self, message, triggering_error=None):
        self._message = message
        self._triggering_error = triggering_error

    def __str__(self):
        return ''.join(['Exception in calling OWM web API.', os.linesep,
                        'Reason: ', self._message, os.linesep,
                        'Caused by: ', str(self._triggering_error)])
