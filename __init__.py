from __future__ import absolute_import
from pyazuresearch.client import AzureSearch
from pyazuresearch.bulkapi import (CreateAd, AdCar)
#from pyazuresearch.settle import Settle


__author__ = 'Pierre Therrode'
__all__ = ['AzureSearch', "CreateAd", "AdCar"]
__version__ = '0.1'
__date__ = '12 November 2014'
__credits__ = "Thanks to Reezocar"
__version_info__ = tuple(__version__.split('.'))
get_version = lambda: __version_info__

