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
    date_t = datetime.datetime.strptime(gmtime, "%a %b %d %H:%M:%S %Y")
    return timegm(date_t.timetuple())


def localtime_to_epoc(localtime):
    """
    Convert localtime to epoc.
    """
    raise NotImplementedError("localtime_to_epoc not implemented: {0}".format(localtime))


def epoc_to_gm_asctime(epoc):
    """
    Convert seconds since epoc to gmtime.
    """
    return time.asctime(time.gmtime(epoc))


def epoc_to_loc_asctime(epoc):
    """
    Convert seconds since epoc to gmtime.
    """
    return time.asctime(time.localtime(epoc))
