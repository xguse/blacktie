# test_whole_run.py is part of the 'blacktie' package.
# It was written by Gus Dunn and was created on 9/9/14.
# 
# Please see the license info in the root folder of this package.

"""
=================================================
test_whole_run.py
=================================================
Purpose:
Tests complete `blacktie`
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


@with_setup(set_up(prefix="test_no_input_"))
def test_no_input():
    wdir = "%s/test_data" % temp_dirs.test_no_input_
    os.chdir(wdir)
    sh.blacktie()

    if not debug:
        shutil.rmtree(wdir)


@with_setup(set_up(prefix="test_bad_option_"))
@raises(ErrorReturnCode)
def test_bad_option():
    wdir = "%s/test_data" % temp_dirs.test_bad_option_
    args = shlex.split("--i-am-not-a-valid-option")
    os.chdir(wdir)
    sh.blacktie(args)

    if not debug:
        shutil.rmtree(wdir)


@with_setup(set_up(prefix="test_multi_progs_"))
def test_multi_progs():
    wdir = "%s/test_data" % temp_dirs.test_multi_progs_
    args = shlex.split("--prog tophat cufflinks --mode analyze %s/test_data/blacktie_config_test.yaml" %
                       wdir)
    os.chdir(wdir)
    sh.blacktie(args)

    if not debug:
        shutil.rmtree(wdir)


@with_setup(set_up(prefix="test_x_"))
def test_x():
    wdir = "%s/test_data" % temp_dirs.test_x_
    args = shlex.split("--prog all --mode analyze %s/test_data/blacktie_config_test.yaml" %
                       wdir)
    os.chdir(wdir)
    sh.blacktie(args)

    if not debug:
        shutil.rmtree(wdir)