"""
RezRxtDbReaderI & RezRxtDbWriterI: rez resolve database reader and writer interfaces.
"""
class RezRxtDbReaderI(object):
    """
    Rez Resolve Database Reader Interface.
    """
    def rxt_dict(self, name, context, timestamp):
        """
        Retrieve a python dictionary matching the name, context, and timestamp.

        Args:
            name (str): Name of the package.
            context (str): Context of the package.
            timestamp (int): Timestamp of the resolve.
        """
        raise NotImplementedError()

    def timestamps(self, name, context):
        """
        Retrieve a list of resolves' timestamps matching the name and context.

        Args:
            name (str): Name of package.
            context (str): Context of package.
        """
        raise NotImplementedError()

    def names(self, context):
        """
        Given a context, return the names of all the resolves tracked by the Rez Resolve DB.
        Args:
            context (str): The context of the resolves.

        Returns:
            List of package names tracked within the context.
        """
        raise NotImplementedError()

    def contexts(self):
        """
        Retrieve all of the contexts in which it is defined.
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
