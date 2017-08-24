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
# uncomment for python3
# from functools import reduce
import json

from rezrxt.dbinterface import RezRxtDbReaderI


class RezRxtDbReadMgr(object):
    """
    Common file db manager operations.
    """
    def __init__(self, root_db):
        """
        Initialize rez resolve database manager with root of database.
        """
        assert isdir(root_db) is True, "root_db \"{0}\" is not a valid directory."
        self._root_db = root_db

    def root_dir(self, verify=False):
        """
        Return the root directory.
        """
        if verify:
            assert isdir(self._root_db) is True, "root_dir() {0} does not exist".format(self._root_db)
        return self._root_db

    def contexts_dir(self, verify=False):
        """
        return the directory which houses all of the contexts.
        """
        c_dir = pjoin(self.root_dir(), "context")
        if verify:
            if isdir(c_dir) is False:
                raise KeyError("contexts_dir() - {0} does not exist".format(c_dir))
        return c_dir

    def context_dir(self, context, verify=False):
        """
        Given a context, return the context directory.

        Args:
            context (str): the context.
            verify (bool): whether to verify the existance of the path (default:False)
        
        Returns:
            path (str).

        Raises:
            KeyError if path does not exist.
        """
        c_dir = pjoin(self._root_db, "context", context)
        if verify:
            if isdir(c_dir) is False:
                raise KeyError("context_dir({0}) {1} does not exist".format(context, c_dir))
        return c_dir

    def names_dir(self, context, verify=False):
        """
        Given a context, return the directory in which the names for said context may be found.
        """

        n_dir = pjoin(self.context_dir(context), "name")
        if verify:
            if isdir(n_dir) is False:
                raise KeyError("names_dir({0}) - {1} does not exist".format(context, n_dir))
        return n_dir

    def name_dir(self, context, name, verify=False):
        """
        Given a context and name, return the full path to the directory.

        Args:
            context (str): the context.
            name (str): name of the package.
            verify (bool): whether to verify the existance of the path (default:False)
   
        Returns:
            path (str).

        Raises:
            KeyError if path directory does not exist and verify is True.
        """
        n_dir = pjoin(self.context_dir(context), "name", name)
        if verify:
            if isdir(n_dir) is False:
                raise KeyError("name_dir({0}, {1}) - {2} does not exist".format(context, name, n_dir))
        return n_dir

    def timestamps_dir(self, context, name, verify=False):
        """
        Return the directory in which the timestamps live.
        """
        t_dir = pjoin(self.name_dir(context, name), "timestamp")
        if verify:
            if isdir(t_dir) is False:
                raise KeyError("timestamps_dir({0}, {1}) - {2} does not exist".format(context, name, t_dir))
        return t_dir

    def timestamp_dir(self, context, name, timestamp, verify=False):
        """
        Given a context, name, and timestamp, return the full path to the directory.

        Args:
            context (str): the context of the package.
            name (str): the name of the package.
            timestamp (int | str): the timestamp of the package.
            verify (bool): Wether to verify the existance of the package. (default: False)

        Returns:
            directory path.

        Raises:
            KeyError - if directory does not exist and verify is True.
        """
        t_dir = pjoin(self.name_dir(context, name), "timestamp", str(timestamp))
        if verify:
            if isdir(t_dir) is False:
                raise KeyError("timestmap_dir({0}, {1}, {2}) {3} does not exist."\
                               .format(context, name, timestamp, t_dir))
        return t_dir

    def rxt_name(self, context, name, timestamp):
        """
        Given appropriate information, construct the name of the rxt file.

        Args:
            context (str): The context of the package.
            name (str): The name of the package.
            timestamp (int): the timestamp of the package resolution.

        Returns:
            The correctly formatted name of the rxt file as stored in the database.
        """
        #assert isinstance (timestamp, (int, long)),
        #   "timestamp should be an integer: {0}".format(timestamp)
        return "{0}-{1}-{2}.rxt".format(context, name, str(timestamp))

    def rxt_path(self, context, name, timestamp, verify=False):
        """
        Build the fullpath of an rxt file given its constituent parts.

        Args:
            context (str): The context of the package.
            name (str): The name of the package.
            timestamp (int): The timestamp of the package resolve.
            verify (bool): whether to verify that the path being constructed, minus the filename, exists.
        
        Returns:
            The path to the rxt file.
        
        Raises:
            KeyError: If a valid path cannot be constructed given the variables.
        """
        return pjoin(self.timestamp_dir(context, name, timestamp, verify),
                     self.rxt_name(context, name, timestamp))

    def contexts(self):
        """
        Return an generator iterator over contexts.
        """
        c_dir = self.contexts_dir()
        if isdir(c_dir) is False:
            # empty repo
            yield None

        for context in listdir(c_dir):
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
        
        namesdir = self.names_dir(context, verify=True)
        
        for name in listdir(namesdir):
            yield name

    def timestamps(self, context, name):
        """
        Returns a generator over timestamps.

        Args:
            context (str): context name.
            name    (str): package name

        Returns:
            Generator over timestamps.

        Raises:
            KeyError: If the database does not contain the context or name.
        """
        tsdir = self.timestamps_dir(context, name, verify=True)
        for tstamp in listdir(tsdir):
            yield int(tstamp)

    def _resolve_approximate(self, context, name, timestamp):
        """
        Return the full path to a resolve given an approximate timestamp.
        """

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
       
        timestamps =  self.timestamps(context, name)
        exact_ts = reduce(tst, (int(x) for x in timestamps))
        if exact_ts == 0:
            timestamps = [x for x in self.timestamps(context, name)]
            timestamps.sort()
            exact_ts = timestamps[0]
            #raise KeyError("unable to resolve exact timestamp from approximate timestamp {0} for {1}"\
            #               .format(timestamp, self.timestamps_dir(context, name, verify=True)))
        return self.rxt_path(context, name, exact_ts, verify=True)

    def _resolve_exact(self, context, name, timestamp):
        """
        Return a full path to a resolve given an exact timestamp.
        """
        return self.rxt_path(context, name, timestamp)


    def resolve(self, context, name, timestamp, approximate=False):
        """
        Return the full path to a resolve.

        Args:
            context      (str): The context name.
            name         (str): The package name.
            timestamp    (int): The timestamp.
            approximate (bool): If true, find the closest timestamp less than or
                                equal to the one provided. If a timestamp is 
                                provided which predates all the available timestamps
                                then we return the smallest extant timestamp.

        Returns:
            Path to rxt file.

        Raises:
            KeyError: If db is missing either the context, name, or timestmap.
        """

        if approximate is True:
            return self._resolve_approximate(context, name, timestamp)
        else:
            return self._resolve_exact(context, name, timestamp)


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
        self.rez_rxt_mgr = RezRxtDbReadMgr(root_db)
        super(RezRxtDbReader, self).__init__()

    def rxt_dict(self, context, name, timestamp, approximate=False):
        """
        Retrieve a python dictionary matching the name, context, and timestamp.

        Args:
            context      (str): Context of the package.
            name         (str): Name of the package.
            timestamp    (int): Timestamp of the resolve.
            approximate (bool): Whether to get the nearest timestamp,
                                less than or equal to timestamp.

        Returns:
            python dict

        Raises:
            RuntimeError if not extant.
        """
        rxt_file = self.rez_rxt_mgr.resolve(context, name, timestamp, approximate)

        with open(rxt_file) as f_handle:
            data = json.load(f_handle)
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
            name    (str): Package name.

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
            context (str): ontext name.
            name    (str): Package name.

        Returns:
            generator over rxt files.

        Raises:
            KeyError: if supplied with non-extant keys.
        """
        for t_stamp in self.rez_rxt_mgr.timestamps(context, name):
            yield self.rez_rxt_mgr.resolve(context, name, t_stamp)

    def resolve(self, context, name, timestamp, approximate=False):
        """
        Get the rxt file matching the parameters
        """
        return self.rez_rxt_mgr.resolve(context, name, timestamp, approximate)