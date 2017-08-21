"""
reader implementation.

We implement a disk-based database with the following structure:
root/
    context/
        name/
            timestamp/
                context-name-timestamp.rxt
"""

from os.path import isdir, isfile
from os.path import join as pjoin
from os import listdir
# done for forward compatibility purposes - with python3
from functools import reduce
import json

from rezrxt.dbinterface import RezRxtDbReaderI


class RezRxtDbMgr(object):
    """
    Common file db manager operations.
    """
    def __init__(self, root_db):
        """
        Initialize rez resolve database manager with root of database.
        """
        assert isdir(root_db) is True, "root_db \"{0}\" is not a valid directory."
        self._root_db = root_db

    def contexts(self):
        """
        Return an generator iterator over contexts.
        """
        for context in listdir(self._root_db):
            yield context

    def names(self, context):
        """
        Given a context name, return an iterator over names.

        Args:
            context (str): The context name. (eg fx, or model)

        Returns:
            name generator

        Raises:
            KeyError: If the db does not contain the supplied context.
        """
        namesdir = pjoin(self._root_db, context)
        if not isdir(namesdir):
            raise KeyError("No packages exist for \"{0}\" context".format(context))
        for name in listdir(namesdir):
            yield name

    def timestamps(self, context, name):
        """
        Returns a generator over timestamps.

        Args:
            context (str): context name.
            name (str): package name

        Returns:
            Generator over timestamps.

        Raises:
            KeyError: If the database does not contain the context or name.
        """
        namesdir = pjoin(self._root_db, context)
        if not isdir(namesdir):
            raise KeyError("No packages exist for \"{0}\" context".format(context))
        tsdir = pjoin(namesdir, name)
        if not isdir(tsdir):
            raise KeyError("No timestamps exist for context:\"{0}\" and name:\"{1}\""\
                          .format(context, name))
        # td: protect from cruft. verify that we are returning an integer.
        for ts in listdir(tsdir):
            yield int(ts)

    def resolve(self, context, name, timestamp, approximate=False):
        """
        Return the full path to a resolve.

        Args:
            context (str): The context name.
            name (str): The package name.
            timestamp (int): The timestamp.
            approximate (bool): If true, find the closest timestamp less than or
                                equal to the one provided.

        Returns:
            Path to rxt file.

        Raises:
            KeyError: If db is missing either the context, name, or timestmap.
        """
        timestamp_str = str(timestamp)

        namesdir = pjoin(self._root_db, context)
        if not isdir(namesdir):
            raise KeyError("No packages exist for \"{0}\" context".format(context))
        tsdir = pjoin(namesdir, name)
        if not isdir(tsdir):
            raise KeyError("No timestamps exist for context:\"{0}\" and name:\"{1}\""\
                .format(context, name))

        resolvedir = None

        if approximate is True:
            # get a find the most
            def tst(xarg, yarg):
                """
                Get the closest value to the timestamp.
                """
                if yarg <= timestamp and xarg <= timestamp:
                    return yarg if yarg >= xarg else xarg
                if yarg <= timestamp:
                    return yarg
                if xarg <= timestamp:
                    return xarg
                return 0

            exact_ts = reduce(tst, (int(x) for x in self.timestamps(context, name)))

            if exact_ts == 0:
                raise RuntimeError("Unable to find exact timestamp for {0} {1} given {2}"\
                                  .format(context, name, timestamp_str))

            resolvedir = pjoin(tsdir, str(exact_ts))
            timestamp_str = str(exact_ts)
            if not isdir(resolvedir):
                raise KeyError(("No resolve exists for context:\"{0}\" name:\"{1}\""
                                "derived timestamp: {2}")\
                              .format(context, name, str(exact_ts)))
        else:
            resolvedir = pjoin(tsdir, timestamp_str)

            if not isdir(resolvedir):
                raise KeyError(("No resolve exists for context:\"{0}\" "
                                "name:\"{1}\" timestamp: {2}")\
                                .format(context, name, str(timestamp)))

        resolve_file = "{0}-{1}-{2}.rxt".format(context, name, timestamp_str)
        resolve_fullpath = pjoin(resolvedir, resolve_file)

        if not isfile(resolve_fullpath):
            raise KeyError(("No rxt file \"{3}\" exists for context:\"{0}\" "
                            "name:\"{1}\" timestamp: {2}")\
                            .format(context, name, str(timestamp), resolve_fullpath))
        return resolve_fullpath


class RezRxtDbReader(RezRxtDbReaderI):
    """
    Database Reader.
    """
    def __init__(self, root_db):
        """
        Args:
            root_db (str): path to root of database.

        Raises:
            AssertionError: If path does not exist.
        """
        self.rez_rxt_mgr = RezRxtDbMgr(root_db)
        super(RezRxtDbReader, self).__init__()

    def rxt_dict(self, context, name, timestamp, approximate=False):
        """
        Retrieve a python dictionary matching the name, context, and timestamp.

        Args:
            context (str): Context of the package.
            name (str): Name of the package.
            timestamp (int): Timestamp of the resolve.
            approximate (bool) : Whether to get the nearest timestamp,
                                 less than or equal to timestamp.

        Returns:
            python dict

        Raises:
            RuntimeError if not extant.
        """
        rxt_file = self.rez_rxt_mgr.resolve(context, name, timestamp, approximate)

        with open(rxt_file) as fh:
            data = json.load(fh)
            return data


    def contexts(self):
        """
        Return a generator of contexts.
        """

        return self.rez_rxt_mgr.contexts()


    def names(self, context):
        """
        Return a generator of names within the supplied context.

        Args:
            context: Context name.

        Returns:
            generator of names.

        Raises:
            KeyError: If context does not exist in DB.
        """
        return self.rez_rxt_mgr.names(context)


    def timestamps(self, context, name):
        """
        Return a generator of timestamps within the supplied context and name.

        Args:
            context (str): Context name.
            name (str): Package name.

        Returns:
            Generator over timestamps.

        Raises:
            KeyError: If supplied with non-extant keys.
        """

        return self.rez_rxt_mgr.timestamps(context, name)

    def rxt_files(self, context, name):
        """
        Return a generator of rxt files.

        Args:
            context (str): context name.
            name (str): Package name.

        Returns:
            generator over rxt files.

        Raises:
            KeyError: if supplied with non-extant keys.
        """
        for t_stamp in self.rez_rxt_mgr.timestamps(context, name):
            yield self.rez_rxt_mgr.resolve(context, name, t_stamp)
