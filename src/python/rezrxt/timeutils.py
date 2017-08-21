"""
timeutils.py - Time Utilities
"""

import time
import datetime
from calendar import timegm

__all__ = ("gmtime_to_epoc", "localtime_to_epoc", "epoc_to_gm_asctime",\
           "epoc_to_loc_asctime")

def gmtime_to_epoc(gmtime):
    """
    Convert gmtime string to epoc time.
    """
    dt = datetime.datetime.strptime(gmtime, "%a %b %d %H:%M:%S %Y")
    return timegm(dt.timetuple())


def localtime_to_epoc(localtime):
    """
    Convert localtime to epoc.
    """
    raise NotImplementedError()


def epoc_to_gm_asctime(epoc):
    """
    Convert seconds since epoc to gmtime.
    """ 
    time.asctime(time.gmtime(x))


def epoc_to_loc_asctime(epoc):
    """
    Convert seconds since epoc to gmtime.
    """ 
    time.asctime(time.localtime(x))
    
    
