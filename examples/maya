#!/usr/bin/env python

"""
wrapper.py - example wrapper code
"""

#from os import environ
from os.path import basename
from os import environ
from sys import argv, path
import argparse

from rezrxt.filebacked import reader
from rez.resolved_context import ResolvedContext
from rezrxt.timeutils import epoc_to_gm_asctime, epoc_to_loc_asctime
from rez.utils.colorize import  critical, heading, local, implicit, Printer

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
    for targ in args:
        for arg in targ:
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
    parser.add_argument("-l", "--list", dest="list_tools", action="store_true",
                        help="list the tools associated with the resolve.")

    args = parser.parse_args(fargs)
    return args
   
def invoke_wrapped_tool():
    """
    Invoke the wrapped tool.

    wrapper.py

    """

    pkg = basename(argv[0])

    parser = argparse.ArgumentParser(prog=pkg,
                                     description='Invoke {0}'.format(pkg))
    parser.add_argument('--rropt', dest='rropt', nargs=1, action='append',
                        metavar=('arg',), help="shot outa luck")
    parser.add_argument('remainder', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    wrapper_args = parse_wrapped_args(pkg, args.rropt)

    ctx = wrapper_args.context or environ.get("REZRXT_CTX")
    if ctx is None:
        print "Need to supply a context or set REZRXT_CTX"
        exit(0)

    tool = wrapper_args.tool
    t_stamp = wrapper_args.timestamp or "now"


    if wrapper_args.list_tools is True:
        if ctx and pkg:
            print ctx, pkg, t_stamp

    print wrapper_args
    print args.remainder

if __name__ == "__main__":
    invoke_wrapped_tool()
