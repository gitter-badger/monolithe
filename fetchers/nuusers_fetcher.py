# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUUsersFetcher(NURESTFetcher):
    """ User fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from courgette.models import NUUser
        return NUUser