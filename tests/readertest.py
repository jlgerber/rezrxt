"""
readertest.py
"""
from os.path import realpath, dirname
from os.path import join as pjoin
import json
import unittest

from rezrxt.filebacked.reader import RezRxtDbReadMgr, RezRxtDbReader

RXT_STR =\
"""
{
    "default_patch_lock": "no_lock",
    "rez_version": "2.12.0",
    "package_requests": [
        "houdini",
        "renderman"
    ],
    "serialize_version": "4.3",
    "resolved_packages": [
        {
            "variables": {
                "index": null,
                "version": "linux",
                "repository_type": "filesystem",
                "location": "/home/jlgerber/packages",
                "name": "platform"
            },
            "key": "filesystem.variant"
        },
        {
            "variables": {
                "index": null,
                "version": "x86_64",
                "repository_type": "filesystem",
                "location": "/home/jlgerber/packages",
                "name": "arch"
            },
            "key": "filesystem.variant"
        },
        {
            "variables": {
                "index": null,
                "version": "CentOS-7.3.1611",
                "repository_type": "filesystem",
                "location": "/home/jlgerber/packages",
                "name": "os"
            },
            "key": "filesystem.variant"
        },
        {
            "variables": {
                "index": 0,
                "version": "16.0.564",
                "repository_type": "filesystem",
                "location": "/rez-packages/ext",
                "name": "houdini"
            },
            "key": "filesystem.variant"
        },
        {
            "variables": {
                "index": 0,
                "version": "21.3",
                "repository_type": "filesystem",
                "location": "/home/jlgerber/packages",
                "name": "renderman"
            },
            "key": "filesystem.variant"
        }
    ],
    "num_loaded_packages": 5,
    "requested_timestamp": null,
    "host": "bigguy.home",
    "user": "jlgerber",
    "package_filter": [],
    "arch": "x86_64",
    "solve_time": 0.010216951370239258,
    "building": false,
    "implicit_packages": [
        "~platform==linux",
        "~arch==x86_64",
        "~os==CentOS-7.3.1611"
    ],
    "parent_suite_path": null,
    "suite_context_name": null,
    "created": 1503265457,
    "graph": "{'nodes': [((('fillcolor', '#AAFFAA'), ('fontsize', 10), ('style', 'filled')), [('_9', 'houdini-16.0.564[0]'), ('_8', 'os-CentOS-7.3.1611[]'), ('_7', 'arch-x86_64[]'), ('_6', 'platform-linux[]'), ('_10', 'renderman-21.3[0]')]), ((('fillcolor', '#F6F6F6'), ('fontsize', 10), ('style', 'filled,dashed')), [('_13', 'os-CentOS-7.3.1611'), ('_12', 'arch-x86_64'), ('_11', 'platform-linux')]), ((('fillcolor', '#FFFFAA'), ('fontsize', 10), ('style', 'filled,dashed')), [('_5', '~os==CentOS-7.3.1611'), ('_4', '~arch==x86_64'), ('_3', '~platform==linux'), ('_2', 'renderman'), ('_1', 'houdini')])], 'edges': [((('arrowsize', '0.5'),), [('_9', '_11'), ('_9', '_13'), ('_9', '_12'), ('_8', '_11'), ('_8', '_12'), ('_5', '_8'), ('_4', '_7'), ('_3', '_6'), ('_2', '_10'), ('_1', '_9'), ('_13', '_8'), ('_12', '_7'), ('_11', '_6'), ('_10', '_13'), ('_10', '_1'), ('_10', '_11'), ('_10', '_12')])]}",
    "failure_description": null,
    "package_orderers": null,
    "package_paths": [
        "/home/jlgerber/packages",
        "/rez-packages/int",
        "/rez-packages/ext"
    ],
    "platform": "linux",
    "rez_path": "/opt/rez-2.12.0/lib/python2.7/site-packages/rez-2.12.0-py2.7.egg/rez",
    "status": "solved",
    "from_cache": false,
    "timestamp": 1503265457,
    "caching": true,
    "load_time": 0.0,
    "os": "CentOS-7.3.1611",
    "patch_locks": {}
}
"""
class RezRxtDbReadMgrTest(unittest.TestCase):
    """
    Tests covering the RezRxtDbMgr.
    """
    def setUp(self):
        """
        Set up.
        """
        self.db_path = pjoin(realpath(dirname(__file__)), "db_root")
        self.mgr = RezRxtDbReadMgr(self.db_path)

    def test_contexts(self):
        """
        Test to see that reader provides correct list of contexts.
        """
        contexts = list(self.mgr.contexts())
        expected = ["fx", "model"]
        self.assertEqual(contexts, expected)

    def test_names(self):
        """
        Validate that one may fetch names given a context.
        """
        names = list(self.mgr.names("model"))
        expected = ["modo", "houdini"]
        names.sort()
        expected.sort()
        self.assertEqual(names, expected)

    def test_timestamps(self):
        """
        Verify that appropriate timestamps are returned.
        """
        timestamps = list(self.mgr.timestamps("model", "houdini"))
        expected = [1503265457, 1503266406]
        self.assertEqual(timestamps, expected)

    def test_resolve(self):
        """
        Test retrieving the full path to a resolve.
        """
        ctx = "model"
        pkg = "houdini"
        t_stamp = 1503265457
        t_stamp_str = str(t_stamp)

        rxt = self.mgr.resolve(ctx, pkg, t_stamp)
        expected = pjoin(self.db_path, ctx, pkg, t_stamp_str,\
                          "{0}-{1}-{2}.rxt".format(ctx, pkg, t_stamp_str))
        self.assertEqual(rxt, expected)


    def test_resolve_approx_1(self):
        """
        Test retrieving the full path to a resolve with an approximate timestamp.
        """
        ctx = "model"
        pkg = "houdini"
        t_stamp_approx = 1503265459
        t_stamp = 1503265457
        t_stamp_str = str(t_stamp)

        rxt = self.mgr.resolve(ctx, pkg, t_stamp_approx, approximate=True)
        expected = pjoin(self.db_path, ctx, pkg, t_stamp_str,\
                          "{0}-{1}-{2}.rxt".format(ctx, pkg, t_stamp_str))
        self.assertEqual(rxt, expected)

    def test_resolve_approx_2(self):
        """
        Test retrieving the full path to a resolve with an approximate timestamp.
        """
        ctx = "model"
        pkg = "houdini"
        t_stamp_approx = 1503266705
        t_stamp = 1503266406
        t_stamp_str = str(t_stamp)

        rxt = self.mgr.resolve(ctx, pkg, t_stamp_approx, approximate=True)
        expected = pjoin(self.db_path, ctx, pkg, t_stamp_str,\
                          "{0}-{1}-{2}.rxt".format(ctx, pkg, t_stamp_str))
        self.assertEqual(rxt, expected)


    def test_resolve_approx_3(self):
        """
        Test retrieving the full path to a resolve with an approximate timestamp.
        When the timestamp is earlier than any of the resolves, we get a RuntimeError.
        """
        ctx = "model"
        pkg = "houdini"
        t_stamp_approx = 1103265459

        with self.assertRaises(RuntimeError):
            self.mgr.resolve(ctx, pkg, t_stamp_approx, approximate=True)


class FileBackedReaderTest(unittest.TestCase):
    """
    Test for rezrxt.filebacked.reader
    """
    def setUp(self):
        self.db_path = pjoin(realpath(dirname(__file__)), "db_root")
        self.reader = RezRxtDbReader(self.db_path)

    def test_rxt_dict(self):
        """
        test the retrieval of a resolve, as a python dict.
        """
        rxt = self.reader.rxt_dict("model", "houdini", 1503265457)
        expected = json.loads(RXT_STR)
        self.assertEqual(rxt, expected)

    def test_rxt_dict_approximate(self):
        """
        test the retrieval of a resolve, as a python dict using the approximate
        timestamp feature. To verify, we make certain that the timestamp provided
        is greater than the earliest timestamp in the directory, but less than the
        latest timestamp in the directory.
        """
        rxt = self.reader.rxt_dict("model", "houdini", 1503265999, approximate=True)
        expected = json.loads(RXT_STR)
        self.assertEqual(rxt, expected)

    def test_contexts(self):
        """
        Test to see that reader provides correct list of contexts.
        """
        contexts = list(self.reader.contexts())
        expected = ["fx", "model"]
        self.assertEqual(contexts, expected)

    def test_names(self):
        """
        Validate that one may fetch names given a context.
        """
        names = list(self.reader.names("model"))
        expected = ["modo", "houdini"]
        names.sort()
        expected.sort()
        self.assertEqual(names, expected)

    def test_timestamps(self):
        """
        Verify that appropriate timestamps are returned.
        """
        timestamps = list(self.reader.timestamps("model", "houdini"))
        expected = [1503265457, 1503266406]
        self.assertEqual(timestamps, expected)

    def test_rxt_files(self):
        """
        verify that we return the correct file list.
        """
        ctx = "model"
        pkg = "houdini"
        t_stamps = ("1503265457", "1503266406")
        files = list(self.reader.rxt_files(ctx, pkg))
        base_path = pjoin(self.db_path, "model", "houdini")
        expected = [pjoin(base_path, t_stamps[0], "{0}-{1}-{2}.rxt".format(ctx, pkg, t_stamps[0])),
                    pjoin(base_path, t_stamps[1], "{0}-{1}-{2}.rxt".format(ctx, pkg, t_stamps[1]))]
        self.assertEqual(files, expected)
