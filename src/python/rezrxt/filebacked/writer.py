"""
writer implementation.
"""

from os.path import isdir, isfile
from os.path import join as pjoin
from os import listdir, makedirs
import json

from rezrxt.dbinterface import RezRxtDbWriterI
from rezrxt.filebacked.reader import RezRxtDbReadMgr
class RezRxtDbWriteMgr(RezRxtDbReadMgr):
    """
    class responsible for updating db.
    """
    def __init__(self, root_db):
        """
        Args:
            root_db (str): path to root of database.

        Raises:
            AssertionError: If root_db does not exist
        """
        super(RezRxtDbWriteMgr, self).__init__(root_db)

    def build_dirs(self, name, context, timestamp):
        """
        Create directory if it does not exist
        """
        makedirs(self.timestamp_dir(context, name, timestamp))

    def write_rxt(self, context, name, timestamp, rxt_dict):
        """
        Write rxt data to directory.
        """
        self.build_dirs(context, name, timestamp)


class RezRxtDbWriter(RezRxtDbWriterI):
    """
    Write rxt to database.
    """
    def __init__(self, root_db, write_mgr_cls=RezRxtDbWriteMgr):
        """
        """
        self.mgr = write_mgr_cls(root_db)



    def add_rxt(self, name, context, rxt_dict):
        """
        Add a resolve for the given name and context. The timestamp
        will be pulled from the rxt_dict

        Args:
            name (str): Name of the package.
            context (str): Context of the package.
            rxt_dict (dict): resolve python dict.

        Raises:
            DuplicateKeyError: If a context already exists with the supplied data.
        """

        timestamp = rxt_dict["timestamp"]
        self.mgr.write_rxt(context, name, str(timestamp), rxt_dict)


    def update_rxt(self, name, context, timestamp, rxt_dict):
        """
        Update an existing resolve, provided one exists matching the supplied keys.
        Args:
            name (str): name of the package.
            context (str): context of the package.
            timestamp (str): timestamp of the resolve.
            rxt_dict (dict): Python dict of the resolve.

        Raises:
            KeyError: if a composite key constructed by the supplied components does not exist.
        """
        raise NotImplementedError()