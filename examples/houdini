#!/usr/bin/env python

"""
wrapper.py - example wrapper code
"""

#from os import environ
from os.path import basename
from os import environ
from sys import argv
import argparse
import time

from rez.resolved_context import ResolvedContext
from rezrxt.filebacked import reader
from rezrxt import constants
#from rezrxt.timeutils import epoc_to_gm_asctime, epoc_to_loc_asctime
#from rez.utils.colorize import  critical, heading, local, implicit, Printer


def invoke_wrapped_tool():
    """
    Invoke the wrapped tool.

    wrapper.py

    """
    # get the package name
    pkg = basename(argv[0])

    # Split args into a tuple of (wrapper_args, package_args)
    all_args = _split_args(argv[1:])

    wrapper_args = parse_wrapped_args(pkg, all_args[0])

    # database
    db_root = wrapper_args.db if wrapper_args and wrapper_args.db\
              else environ.get(constants.REZRXT_DB_ROOT)

    if db_root is None:
        print "Need to set {0} or set db via --rropt".format(constants.REZRXT_DB_ROOT)
        exit(0)

    # Context
    ctx = wrapper_args.context if (wrapper_args and wrapper_args.context)\
          else environ.get(constants.REZRXT_CTX)
    if ctx is None:
        print "Need to supply a context via --rropt set {0} env var".format(constants.REZRXT_CTX)
        exit(0)

    # Timestamp
    t_stamp = wrapper_args.timestamp or time.time()

    if wrapper_args.list_tools is True:
        _list_tools(db_root, ctx, pkg, t_stamp)

     # tool
    tool = wrapper_args.tool

    print wrapper_args
    print all_args[1]

def _split_args(args):
    """
    Given a list of args, split it into two list - the first a list of
    rezrxt arguements, and the second the remainder.

    Args:
        args (list): a list of arguements (normally argv[1:])

    Returns:
        ([], [])
    """
    all_args = ([], [])
    wargb = False
    for an_arg in args:
        if wargb is True:
            all_args[0].append(an_arg)
            wargb = False
            continue
        if an_arg == "--rropt":
            wargb = True
            continue
        all_args[1].append(an_arg)
    return all_args

def _list_tools(db_root, ctx, pkg, t_stamp):
    """
    List the tools.
    """
    try:
        t_gen = get_tools(db_root, ctx, pkg, t_stamp)
        list_tools(t_gen)
    except (KeyError, RuntimeError), err:
        print err.message
    exit(0)

def parse_wrapped_args(name, args):
    """
    Parse the wrapped arguments in a second pass.

    OPTIONS
    -t --time <timestamp> If not provided, assume we want the latest solve
    -c --context <context> or get from environment
    -d --db rez rxt database
    -t --tool <name> tool
    -l --list list tools
    """
    if args is None:
        return None
    fargs = []

    for arg in args:
        pieces = arg.split(',')
        for piece in pieces:
            no_eq = piece.split('=')
            fargs.append("{0}{1}".format(("--" if len(no_eq[0]) > 1 else "-"), piece))
    parser = argparse.ArgumentParser(prog="{0} wrapper".format(name),\
             description='Process wrapper arguments and invoke {0}'.format(name))
    parser.add_argument("--ts", "--time", dest="timestamp",
                        help="Time to invoke {0} at".format(argv[0]))
    parser.add_argument("-c", "--context", dest="context",
                        help="Context within which to invoke {0}".format(argv[0]))
    parser.add_argument("-d", "--db", dest="db", help="Path to a database root directory")
    parser.add_argument("-t", "--tool", dest="tool", help="The tool to invoke")
    parser.add_argument("-l", "--list", "--list-tools", dest="list_tools", action="store_true",
                        help="list the tools associated with the resolve.")

    args = parser.parse_args(fargs)
    return args


def list_tools(t_gen):
    """
    Given a tools generator, print the names of the tools
    """
    try:
        for pkg_name, tools in t_gen:
            print pkg_name
            for t_name in tools[1]:
                print "\t{0}".format(t_name)
    except KeyError, err:
        print err.message
        exit(0)

def get_tools(db_root, ctx, pkg, timestamp):
    """
    Given the appropriate information, list the tools available.

    Args:
        db_root (str): Path to the root of the database.
        ctx (str): The context.
        pkg (str): The package.
        timestamp (int): The timestamp in seconds since Jan 1, 1970

    Returns:
        generator of iterator over tools

    Raises:
        KeyError, RuntimeError
    """
    db_reader = reader.RezRxtDbReader(db_root)

    rxt_f = db_reader.resolve(ctx, pkg, timestamp, approximate=True)
    resolved = ResolvedContext.load(rxt_f)

    return resolved.get_tools().iteritems()


if __name__ == "__main__":
    invoke_wrapped_tool()
