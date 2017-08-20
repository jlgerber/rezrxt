"""
rezrxt - system for handling rez rxt files based on date.
"""


class RezRxtDbReaderI(object):
    """
    Rez Resolve Database Reader Interface.
    """
    def get_rxt(self, name, context, timestamp):
        """
        Retrieve a python dictionary matching the name, context, and timestamp.

        Args:
          name (str): Name of the package.
          context (str): Context of the package.
          timestamp (int): Timestamp of the resolve.
        """
        raise NotImplementedError()

    def get_rxt_timestamps(self, name, context):
        """
        Retrieve a list of resolves' timestamps matching the name and context.
        
        Args:
          name (str): Name of package.
          context (str): Context of package.
        """
        raise NotImplementedError()

    def get_rxt_names(self, context):
        """
        Given a context, return the names of all the resolves tracked by the Rez Resolve DB.
        Args:
          context (str): The context of the resolves.
        
        Returns:
           List of package names tracked within the context.
        """
        raise NotImplementedError()

    def get_rxt_contexts(self, name):
        """
        Given a package name, retrieve all of the contexts in which it is defined.
        Args:
          name (str): The name of the package.
        
        Returns:
          A list of contexts.
        """
        raise NotImplementedError()


class RezRxtDbWriterI(object):
    """
    Rez Resovle Database Writer Interface.
    """
    def add_rxt(self, name, context, timestamp, rxt_dct):
        """
        Add a resolve for the given name, context, and timestamp.

        Args:
          name (str): Name of the package.
          context (str): Context of the package.
          timestmap: timestamp of the resolve.
          rxt_dct (dict): resolve python dict.

        Raises:
          DuplicateKeyError: If a context already exists with the supplied data.
        """
        raise NotImplementedError()

    def update_rxt(self, name, context, timestamp, rxt_dct):
        """
        Update an existing resolve, provided one exists matching the supplied keys.
        Args:
          name (str): name of the package.
          context (str): context of the package.
          timestamp (str): timestamp of the resolve.
          rxt_dct (dict): Python dict of the resolve.

        Raises:
          KeyError: if a composite key constructed by the supplied components does not exist.
        """
        raise NotImplementedError()


class RezRxtManager(object):
    """
    manage rez's rxt files. 
    """
    def __init__(self, rez_rxt_db):
        self._rez_rxt_db = rez_rxt_db

'''
        """
        Args:
          context (str): Context in which the resolve applies.
          name (str) : Name of the package to which the resolve applies.
          time (time): Time which we are interested in.
        """
        self._context = context
        self._name = name
        self._time = time
'''
