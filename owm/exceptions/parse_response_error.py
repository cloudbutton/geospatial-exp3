"""
Module containing ParseResponseError class

AUTHOR: Juanjo

DATE: 08/01/2018

"""

import os

from . import OWMError


class ParseResponseError(OWMError):
    """
    Error class that represents failures when parsing payload data in HTTP
    responses sent by the OWM web API.

    :param str message: the message of the error
    :returns: a *ParseResponseError* instance

    """

    def __init__(self, message):
        self._message = message

    def __str__(self):
        return ''.join(['Exception in parsing OWM web API response',
                        os.linesep, 'Reason: ', self._message])
