#*****************************************************************************
#  blacktie_pipeline.py (part of the blacktie package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licenced under the GNU General Public License 3.0 license.
#******************************************************************************

"""
####################
blacktie_pipeline.py
####################
Code defining an object oriented python pipeline script to allow simplified
coordination of data through parts or all of the popular Tophat/Cufflinks
RNA-seq analysis suite.
"""

import os
import sys
import argparse
import base64
import traceback
import re
import time
import socket
import shutil
from collections import defaultdict

import yaml

try:
    import pprocess
except ImportError:
    pass

import blacktie

from blacktie.utils.misc import Bunch,bunchify
from blacktie.utils.misc import email_notification
from blacktie.utils.misc import get_time
from blacktie.utils.misc import map_condition_groups

from blacktie.utils.externals import runExternalApp
from blacktie.utils.externals import mkdirp

from blacktie.utils import errors
from blacktie.utils.calls import *


def main():
    """
    The main loop.  Lets ROCK!
    """

    desc = """This script reads options from a yaml formatted file and organizes the execution of tophat/cufflinks runs for multiple condition sets."""

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--version', action='version', version='%(prog)s ' + blacktie.__version__,
                        help="""Print version number.""")    
    parser.add_argument('config_file', type=str,
                        help="""Path to a yaml formatted config file containing setup options for the runs.""")
    parser.add_argument('--prog', type=str, choices=['tophat','cufflinks','cuffmerge','cuffdiff','cummerbund','all'], default='tophat',
                        help="""Which program do you want to run? (default: %(default)s)""")
    parser.add_argument('--hide-logs', action='store_true', default=False,
                        help="""Make your log directories hidden to keep a tidy 'looking' base directory. (default: %(default)s)""")
    parser.add_argument('--no-email', action='store_true', default=False,
                        help="""Don't send email notifications. (default: %(default)s)""")
    parser.add_argument('--mode', type=str, choices=['analyze','dry_run','qsub_script'], default='analyze',
                        help="""1) 'analyze': run the analysis pipeline. 2) 'dry_run': walk through all steps that
                        would be run and print out the command lines; however, do not send the commands to the
                        system to be run. 3) 'qsub_script': generate bash scripts suitable to be sent to a compute cluster's
                        SGE through the qsub command. (default: %(default)s)""")    

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()

    yargs = bunchify(yaml.load(open(args.config_file,'rU')))

    # set up run_id, log files, and email info
    if yargs.run_options.run_id:
        run_id = yargs.run_options.run_id
    else:

        run_id = get_time()

    base_dir = yargs.run_options.base_dir.rstrip('/')
    if args.hide_logs:
        run_logs  = '%s/.%s.logs' % (base_dir,run_id)
    else:
        run_logs  = '%s/%s.logs' % (base_dir,run_id)


    if not args.mode == 'dry_run':
        mkdirp(run_logs)
    else:
        pass


    yaml_out = '%s/%s.yaml' % (run_logs,run_id)



    # copy yaml config file with run_id as name for records
    if not args.mode == 'dry_run':
        shutil.copyfile(args.config_file,yaml_out)
    else:
        pass

    if not args.no_email:
        email_info = Bunch({'email_from' : yargs.run_options.email_info.sender,
                            'email_to' : yargs.run_options.email_info.to,
                            'email_li' : open(yargs.run_options.email_info.li,'rU').readline().rstrip('\n')})
    else:
        email_info = Bunch({'email_from' : False,
                            'email_to' : False,
                            'email_li' : ''})

    yargs.prgbar_regex = re.compile('>.+Processing.+\[.+\].+%\w*$')
    yargs.groups = map_condition_groups(yargs)
    yargs.call_records = {}

    # loop through the queued conditions and send reports for tophat 
    if args.prog in ['tophat','all']:
        print '[Note] Starting tophat step.\n'
        for condition in yargs.condition_queue:

            # Prep Tophat Call
            tophat_call = TophatCall(yargs,email_info,run_id,run_logs,conditions=condition,mode=args.mode)
            tophat_call.execute()

            # record the tophat_call object
            yargs.call_records[tophat_call.call_id] = tophat_call
    else:
        print "[Note] Skipping tophat step.\n"

    if args.prog in ['cufflinks','all']:
        # attempt to run more than one cufflinks call in parallel since cufflinks
        # seems to use only one processor no matter the value of -p you give it and
        # doesn't seem to consume massive amounts of memory 
        print "[Note] Starting cufflinks step.\n"
        try:
            if args.mode == 'dry_run':
                raise errors.BlacktieError("dry run")
            queue = pprocess.Queue(limit=yargs.cufflinks_options.p)

            def run_cufflinks_call(cufflinks_call):
                """
                function to start each parallel cufflinks_call inside the parallel job server.
                """
                cufflinks_call.execute()
                return cufflinks_call

            def change_processor_count(cufflinks_call):
                """
                Since we will run multiple instances of CufflinksCall at once, reduce
                the number of processors any one system call thinks it can use.
                """
                cufflinks_call.opt_dict['p'] = 2
                cufflinks_call.construct_options_list()
                cufflinks_call.options_list.extend([cufflinks_call.accepted_hits])
                cufflinks_call.arg_str = ' '.join(cufflinks_call.options_list)
                return cufflinks_call

            execute = queue.manage(pprocess.MakeParallel(run_cufflinks_call))
            jobs = []
            for condition in yargs.condition_queue:
                cufflinks_call = CufflinksCall(yargs,email_info,run_id,run_logs,conditions=condition,mode=args.mode)
                cufflinks_call = change_processor_count(cufflinks_call)
                jobs.append(cufflinks_call)
                execute(cufflinks_call)

            # record the cufflinks_call objects
            for call in queue:
                yargs.call_records[call.call_id] = call

        except (NameError, errors.BlacktieError) as exc:

            if (str(exc) != "name 'pprocess' is not defined") and (str(exc) != "dry run"):
                raise exc
            else:
                print "Running cufflinks in serial NOT parallel.\n"
                # loop through the queued conditions and send reports for cufflinks    
                for condition in yargs.condition_queue:   
                    # Prep cufflinks_call
                    cufflinks_call = CufflinksCall(yargs,email_info,run_id,run_logs,conditions=condition,mode=args.mode)
                    cufflinks_call.execute()

                    # record the cufflinks_call object
                    yargs.call_records[cufflinks_call.call_id] = cufflinks_call
    else:
        print "[Note] Skipping cufflinks step.\n"



    if args.prog in ['cuffmerge','all']:
        print "[Note] Starting cuffmerge step.\n"
        for exp_id in yargs.groups:
            
            # Prep cuffmerge call
            cuffmerge_call = CuffmergeCall(yargs,email_info,run_id,run_logs,conditions=exp_id,mode=args.mode)
            cuffmerge_call.execute()

            # record the cuffmerge_call object
            yargs.call_records[cuffmerge_call.call_id] = cuffmerge_call

    else:
        print "[Note] Skipping cuffmerge step.\n"


    if args.prog in ['cuffdiff','all']:
        print "[Note] Starting cuffdiff step.\n"
        for exp_id in yargs.groups:

            # Prep cuffmerge call
            cuffdiff_call = CuffdiffCall(yargs,email_info,run_id,run_logs,conditions=exp_id,mode=args.mode)
            cuffdiff_call.execute()

            # record the cuffdiff_call object
            yargs.call_records[cuffdiff_call.call_id] = cuffdiff_call

    else:
        print "[Note] Skipping cuffdiff step.\n"    


    if args.prog in ['cummerbund','all']:
        
        # test to make sure R and cummeRbund libs exist
        from blacktie.scripts import cummerbund
        cummerbund.import_cummeRbund_library()
        
        print "[Note] Starting cummerbund step.\n"
        for exp_id in yargs.groups:

            # Prep cummerbund call
            cummerbund_call = CummerbundCall(yargs,email_info,run_id,run_logs,conditions=exp_id,mode=args.mode)
            cummerbund_call.execute()

            # record the cummerbund_call object
            yargs.call_records[cummerbund_call.call_id] = cummerbund_call

    else:
        print "[Note] Skipping cummerbund step.\n"


if __name__ == "__main__":
    main()