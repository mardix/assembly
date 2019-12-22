# -*- coding: utf-8 -*-
"""
Assembly views

"""

from assembly import (Assembly, HTTPError)

# ------------------------------------------------------------------------------


class Error(Assembly):
    """
    This View handles errors
    """

    def _error_handler(self, e):
        """
        * special method
        Error handler method to catch all HTTP Error
        It's template must be the same name without the leading _, ie 'error_handler.html'
        """
        return {
            "code": e.code,
            "e": e
        }

    def _error_404(self, e):
        """
        * special method
        Error handler for 404
        It's template must be the same name without the leading _, ie 'error_404.html'
        """
        return {
            "code": e.code,
            "e": e
        }
