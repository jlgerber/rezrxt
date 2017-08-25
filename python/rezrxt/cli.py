"""
wrapper functions.
"""

__all__ = ("invoke_wrapped_tool",)

#from os import environ
from os.path import basename
from os import environ
from sys import argv, stderr, stdin
import argparse
import time
import select

from rez.resolver import ResolverStatus
from rez.system import system
from rez.shells import get_shell_types
from rez.resolved_context import ResolvedContext
from rez.vendor.argparse import SUPPRESS

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
        print >> stderr, "Need to set {0} or set db via --rropt".format(constants.REZRXT_DB_ROOT)
        exit(1)
    
    db_reader = reader.RezRxtDbReader(db_root)

    # Context
    ctx = wrapper_args.context if (wrapper_args and wrapper_args.context)\
          else environ.get(constants.REZRXT_CTX)
    if ctx is None:
        print >> stderr, "Need to supply a context via --rropt set {0} env var".format(constants.REZRXT_CTX)
        exit(1)

    # Timestamp
    t_stamp = wrapper_args.timestamp or int(time.time())

    if wrapper_args.list_tools is True:
        _list_tools(db_root, ctx, pkg, t_stamp)

     # tool
    tool = wrapper_args.tool

    rxt_dict = db_reader.rxt_dict(ctx, pkg, t_stamp, True)

    context = ResolvedContext.from_dict(rxt_dict, db_reader.read_mgr.rxt_name(ctx, pkg, t_stamp))

    if context.status != ResolverStatus.solved:
        print >> stderr, "cannot rez-env into a failed context"
        exit(1)

    # from rez
    '''
     # generally shells will behave as though the '-s' flag was not present when
    # no stdin is available. So here we replicate this behaviour.
    if opts.stdin and not select.select([sys.stdin], [], [], 0.0)[0]:
        opts.stdin = False

    quiet = opts.quiet or bool(command)
    returncode, _, _ = context.execute_shell(
        shell=opts.shell,
        rcfile=opts.rcfile,
        norc=opts.norc,
        command=command,
        stdin=opts.stdin,
        quiet=quiet,
        start_new_session=opts.new_session,
        detached=opts.detached,
        pre_command=opts.pre_command,
        block=True)

    sys.exit(returncode)
    '''
    #
    # from rez.cli.env.py
    #
    # generally shells will behave as though the '-s' flag was not present when
    # no stdin is available. So here we replicate this behaviour.
    if wrapper_args.stdin and not select.select([stdin], [], [], 0.0)[0]:
        wrapper_args.stdin = False

    cmd = [tool or pkg]
    cmd.extend(all_args[1])

    quiet = False if wrapper_args.verbose else True

    returncode, _, _ = context.execute_shell(
        shell=wrapper_args.shell,
        rcfile=wrapper_args.rcfile,
        norc=wrapper_args.norc,
        command=cmd,
        stdin=wrapper_args.stdin,
        quiet=quiet,
        start_new_session=wrapper_args.new_session,
        detached=wrapper_args.detached,
        pre_command=wrapper_args.pre_command,
        block=True)
    return returncode

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
        print >> stderr, err.message
    exit(1)

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
    shells = get_shell_types()

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
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "--shell", dest="shell", type=str, choices=shells,
        default=system.shell,
        help="target shell type (default: %(default)s)")
    parser.add_argument(
        "--rcfile", type=str,
        help="source this file instead of the target shell's standard startup "
        "scripts, if possible")
    parser.add_argument(
        "--norc", action="store_true",
        help="skip loading of startup scripts")
    parser.add_argument(
        "-s", "--stdin", action="store_true",
        help="read commands from standard input")
    parser.add_argument(
        "--new-session", action="store_true",
        help="start the shell in a new process group")
    parser.add_argument(
        "--detached", action="store_true",
        help="open a separate terminal")
    parser.add_argument(
        "--pre-command", type=str, help=SUPPRESS)

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
        print >> stderr, err.message
        exit(1)

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
