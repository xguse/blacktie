# test_blacktie_cummerbund.py is part of the 'tsetseDB' package.
# It was written by Gus Dunn and was created on 9/10/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_blacktie_cummerbund.py
=================================================
Purpose:

"""
__author__ = 'Gus Dunn'

# test_whole_run.py is part of the 'blacktie_cummerbund' package.
# It was written by Gus Dunn and was created on 9/9/14.
#
# Please see the license info in the root folder of this package.

"""
=================================================
test_whole_run.py
=================================================
Purpose:
Tests complete `blacktie_cummerbund`
"""
__author__ = 'Gus Dunn'

import os
from tempfile import mkdtemp
import shutil
import shlex
from distutils.dir_util import copy_tree as dutils_cp_tree

from nose.tools import raises, with_setup

from sh import ErrorReturnCode
import sh

from bunch import Bunch

debug = False

current_directory = os.getcwd()

temp_dirs = Bunch()


def set_up(prefix):
    """set up test fixtures"""
    tmpdir = mkdtemp(prefix=prefix)
    temp_dirs[prefix] = tmpdir

    # Copy test_data to tmp dir
    src_dir = "%s/test_data" % current_directory
    dst_dir = "%s/test_data" % tmpdir
    dutils_cp_tree(src_dir, dst_dir)


def tear_down():
    """tear down test fixtures"""
    pass


@with_setup(set_up(prefix="test_no_input_"))
def test_no_input():
    wdir = "%s/test_data" % temp_dirs.test_no_input_
    os.chdir(wdir)
    sh.blacktie_cummerbund()

    if not debug:
        shutil.rmtree(wdir)


@with_setup(set_up(prefix="test_bad_option_"))
@raises(ErrorReturnCode)
def test_bad_option():
    wdir = "%s/test_data" % temp_dirs.test_bad_option_
    args = shlex.split("--i-am-not-a-valid-option")
    os.chdir(wdir)
    sh.blacktie_cummerbund(args)

    if not debug:
        shutil.rmtree(wdir)


@with_setup(set_up(prefix="test_blacktie_call_settings_"))
def test_x():
    wdir = "%s/test_data" % temp_dirs.test_blacktie_call_settings_
    args = shlex.split("--file-type pdf "
                       "--cuffdiff-dir %(base_dir)s/blacktie_test_ref/cuffdiff_ctrl_0.ctrl_1.exp_0.exp_1 "
                       "--out %(base_dir)s/cummerbund_plots "
                       "--gtf-path %(base_dir)s/blacktie_test_ref/cuffmerge_ctrl_0.ctrl_1.exp_0.exp_1/merged.gtf" %
                       {"base_dir": wdir})
    os.chdir(wdir)
    sh.blacktie_cummerbund(args)

    if not debug:
        shutil.rmtree(wdir)