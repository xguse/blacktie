#*****************************************************************************
#  calls.py (part of the blacktie package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licenced under the GNU General Public License 2.0 license.
#******************************************************************************

"""
####################
calls.py
####################
Code defining classes to represent and excute pipeline program calls.
"""

from blacktie.utils.misc import Bunch,bunchify
from blacktie.utils.misc import email_notification
from blacktie.utils.externals import runExternalApp
from blacktie.utils import errors


class BaseCall(object):
    """
    Defines common methods for all program call types.
    """
    def __init__(self,yargs,email_info,run_id,run_log,run_err,conditions):
        """
        *GIVEN*:
            * x
        *DOES*:
            * x
        """
        self._hostname = socket.gethostname()
        self.yargs = yargs
        self.email_info = email_info
        self.run_id = run_id
        self.stdout = run_log
        self.stderr = run_err
        self.prgbar_regex = yargs.prgbar_regex
        self._conditions = conditions
        self.prog_yargs = None # over-ride in child __init__
        self.arg_str = None # over-ride in child __init__




    def _flag_out_dir(self):
        """
        *Does:*
            * renames out directory, prepending 'FAILED' flag: ``mv tophat_Aa0 FAILED.tophat_Aa0``
        """
        orig_path_tokens = os.path.abspath(self.out_dir).split('/')[1:]
        new_path = "/%s/FAILED.%s" % ('/'.join(orig_path_tokens[:-1]), orig_path_tokens[-1])
        os.rename(os.path.abspath(self.out_dir),new_path)
        self.out_dir = new_path


    def set_call_id(self):
        if isinstance(self._conditions,int) or isinstance(self._conditions,str):
            # this should mean that we are dealing with a "group" type call
            self.group_id = self._conditions
            self._conditions = self.yargs.groups[self.group_id]
            condition_names = [x.name for x in self._conditions]
            call_id = "%s_%s" % (self.prog_name,"-".join(condition_names))
            self.call_id = call_id

        elif isinstance(self._conditions,dict):
            condition_name = self._conditions['name']
            call_id = "%s_%s" % (self.prog_name,condition_name)
            self.call_id = call_id
        else:
            raise

    def notify_start_of_call(self):
        e = self.email_info
        report_time = runExternalApp('date',"+'%Y%m%d_%H:%M'")[0].strip('\n')
        email_sub="[SITREP from %s] Run %s - Starting %s at %s" % (self._hostname,self.run_id,self.call_id,report_time)
        email_body="%s\n\n%s" % (email_sub,self.cmd_string)
        email_notification(e.email_from, e.email_to, email_sub, email_body, base64.b64decode(e.email_li))

    def notify_end_of_call(self):
        e = self.email_info

        report_time = runExternalApp('date',"+'%Y%m%d_%H:%M'")[0].strip('\n')
        email_sub="[SITREP from %s] Run %s - Exited %s at %s" % (self._hostname,self.run_id,self.call_id,report_time)

        #    repeat subject in body
        email_body=email_sub
        email_body += "\n\n ==> stdout <==\n\n%s" % (self.stdout_msg)

        email_body += "\n\n ==> stderr <==\n\n%s" % (self.stderr_msg)
        email_notification(e.email_from, e.email_to, email_sub, email_body, base64.b64decode(e.email_li))

    def build_out_dir_path(self):
        """
        *DOES:*
            * builds correct ``out_dir`` path based on state of ``self``.
        *RETURNS:*
            * ``out_dir``
        """

        base_dir = self.yargs.run_options.base_dir.rstrip('/')
        return "%s/%s" % (base_dir,self.call_id)

    def init_opt_dict(self):
        """
        *DOES:*
            * based on option names in the yaml file for this phase,
              build a dict with non-job-specific values set and job-specific
              values set to False
        *RETURNS:*
            * partially populated ``opt_dict``
        """
        opt_dict = defaultdict(bool)
        for opt in self.prog_yargs.keys():
            opt_dict[opt]
        opt_dict = dict(opt_dict) # from now on I want missing keys to raise error

        # Populate opt_dict with non-job-specific options encoded in yaml file
        # Ignore positional args for now
        no_positional_args = self.prog_yargs.keys()
        no_positional_args.remove('positional_args')

        for opt in no_positional_args:
            opt_val = self.prog_yargs[opt]
            if opt_val != "from_conditions":
                opt_dict[opt] = opt_val
        return opt_dict

    def construct_options_list(self):
        """
        *DOES:*
            * converts ``opt_dict`` into list encoding proper options to send to the current program: saves to ``self``.
        """
        options_list = []
        for opt in self.opt_dict:
            if self.opt_dict[opt] is False:
                continue
            else:
                pass

            if len(opt) == 1:
                options_list.append('-%s' % (opt))
            else:
                options_list.append('--%s' % (opt))

            opt_val_str = str(self.opt_dict[opt])
            if opt_val_str != 'True':
                options_list.append(opt_val_str)

        self.options_list = options_list

    def purge_progress_bars(self, stderr_str):
        lines = stderr_str.split('\n')
        no_bar = []
        for line in lines:
            if self.prgbar_regex.search(line) != None: # prgbar regex compiled outside scope to avoid re-complilation overhead
                pass
            else:
                no_bar.append(line)
        return '\n'.join(no_bar)

    def log_msg(self,out_msg='',err_msg=''):
        out = open(self.stdout,'a')
        err = open(self.stderr,'a')
        out.write('\n%s\n' % (out_msg))
        err.write('\n%s\n' % (err_msg))
        out.close()
        err.close()    

    def log_start(self):
        msg = '[start %s]\n' % (self.call_id)
        self.log_msg(out_msg=msg,err_msg=msg)

    def log_end(self):

        self.stderr_msg = self.purge_progress_bars(self.stderr_msg)

        out_msg = "%s\n\n%s\n[end %s]\n\n" % (self.cmd_string,self.stdout_msg,self.call_id)
        err_msg = "%s\n\n%s\n[end %s]\n\n" % (self.cmd_string,self.stderr_msg,self.call_id)
        self.log_msg(out_msg,err_msg)

    def execute(self):
        """
        *DOES:*
            * calls correct program, records results, and manages errors.
        """
        self.cmd_string = "%s %s" % (self.prog_name,self.arg_str)
        try:
            self.notify_start_of_call()
            self.log_start()

            self.stdout_msg,self.stderr_msg = runExternalApp(progName=self.prog_name,argStr=self.arg_str)

            self.log_end()
            self.notify_end_of_call()
        except Exception as exc:
            email_body = traceback.format_exc()
            email_body = self.purge_progress_bars(email_body)
            e = self.email_info

            self.stdout_msg = "\nError in call.  Check error log.\n"
            self.stderr_msg = email_body

            self.log_end()

            self._flag_out_dir()

            if isinstance(exc,errors.SystemCallError):
                email_sub="[SITREP from %s] Run %s experienced SystemCallError in call %s. MOVING ON." % (self._hostname,self.run_id,self.call_id)
                email_notification(e.email_from, e.email_to, email_sub, email_body, base64.b64decode(e.email_li))                
            elif isinstance(exc,KeyboardInterrupt):
                email_sub="[SITREP from %s] Run %s experienced KeyboardInterrupt in call %s. MOVING ON." % (self._hostname,self.run_id,self.call_id)
                email_notification(e.email_from, e.email_to, email_sub, email_body, base64.b64decode(e.email_li)) 
            else:
                email_sub="[SITREP from %s] Run %s experienced unhandled exception in call %s. EXITING." % (self._hostname,self.run_id,self.call_id)
                email_notification(e.email_from, e.email_to, email_sub, email_body, base64.b64decode(e.email_li))
                raise
        finally:
            return True


class TophatCall(BaseCall):
    """
    Manage a single call to tophat and store associated run data.
    """

    def __init__(self,yargs,email_info,run_id,run_log,run_err,conditions):

        self.prog_name = 'tophat'

        BaseCall.__init__(self,yargs,email_info,run_id,run_log,run_err,conditions)

        self.prog_yargs = self.yargs.tophat_options
        self.set_call_id()
        self.out_dir = self.get_out_dir()

        # set up options for program call
        self.opt_dict = self.init_opt_dict()
        self.opt_dict['o'] = self.out_dir
        self.opt_dict['G'] = self.get_gtf_anno()
        self.construct_options_list()

        # now the positional args
        bowtie_index = self.get_bt_idx()
        left_reads = self.get_lt_reads()
        right_reads = self.get_rt_reads()

        # combine and save arg_str
        self.options_list.extend([bowtie_index,left_reads,right_reads])
        self.arg_str = ' '.join(self.options_list)

    def get_out_dir(self):
        option = self.prog_yargs.o
        if option == 'from_conditions':
            return self.build_out_dir_path()
        else:
            return option

    def get_gtf_anno(self):
        option = self.prog_yargs.G
        if option == 'from_conditions':
            gtf_path = self._conditions['gtf_annotation']
            return gtf_path
        else:
            return option

    def get_bt_idx(self):
        option = self.prog_yargs.positional_args.bowtie2_index
        if option == 'from_conditions':
            bt_idx_dir = self.yargs.run_options.bowtie_indexes_dir.rstrip('/')
            bt_idx_name = self._conditions['bowtie2_index']
            return "%s/%s" % (bt_idx_dir,bt_idx_name)
        else:
            return option

    def get_lt_reads(self):
        option = self.prog_yargs.positional_args.left_reads
        if option == 'from_conditions':
            lt_reads = self._conditions['left_reads']
            return "%s" % (','.join(lt_reads))
        else:
            return option

    def get_rt_reads(self):
        option = self.prog_yargs.positional_args.right_reads
        if option == 'from_conditions':
            rt_reads = self._conditions['right_reads']
            return "%s" % (','.join(rt_reads))
        else:
            return option


class CufflinksCall(BaseCall):
    """
    Manage a single call to cufflinks and store associated run data.
    """

    def __init__(self,yargs,email_info,run_id,run_log,run_err,conditions):

        self.prog_name = 'cufflinks'

        BaseCall.__init__(self,yargs,email_info,run_id,run_log,run_err,conditions)

        self.prog_yargs = self.yargs.cufflinks_options
        self.set_call_id()
        self.out_dir = self.get_out_dir()


        # set up options for program call
        self.opt_dict = self.init_opt_dict()
        self.opt_dict['o'] = self.out_dir
        self.opt_dict['GTF-guide'] = self.get_gtf_anno()
        self.opt_dict['frag-bias-correct'] = self.get_genome()
        self.opt_dict['mask-file'] = self.get_mask_file()
        self.construct_options_list()

        # now the positional args
        self.accepted_hits = self.get_accepted_hits() 

        # combine and save arg_str
        self.options_list.extend([self.accepted_hits])
        self.arg_str = ' '.join(self.options_list)

    def get_out_dir(self):
        option = self.prog_yargs.o
        if option == 'from_conditions':
            return self.build_out_dir_path()
        else:
            return option

    def get_gtf_anno(self):
        option = self.prog_yargs['GTF-guide']
        if option == 'from_conditions':
            gtf_path = self._conditions['gtf_annotation']
            return gtf_path
        else:
            return option

    def get_genome(self):
        option = self.prog_yargs['frag-bias-correct']
        if option == 'from_conditions':
            genome_path = self._conditions['genome_seq']
            return genome_path
        else:
            return option

    def get_accepted_hits(self):
        option = self.prog_yargs.positional_args.accepted_hits
        if option == 'from_conditions':
            bam_path = self.get_bam_path()
            return bam_path
        else:
            return option

    def get_bam_path(self):
        th_call_id = "tophat_%s" % (self._conditions['name'])
        try:
            th_call = self.yargs.call_records[th_call_id]
            th_out_dir = th_call.out_dir
            bam_path = "%s/accepted_hits.bam" % (th_out_dir.rstrip('/'))
        except (KeyError,AttributeError) as exp:
            msg = "WARNING: unable to find matching tophat call record in memory for condition: %s\nAttempting to find corresponding cufflinks outfile in your base_dir." \
                % (self._conditions['name'])            
            self.log_msg(err_msg=msg)

            # try to guess correct tophat out directory
            base_dir = self.yargs.run_options.base_dir
            bam_path = "%s/%s/accepted_hits.bam" % (base_dir.rstrip('/'),th_call_id)
            if not os.path.exists(bam_path):
                # TODO: build framework to handle this non-fatally
                raise errors.MissingArgumentError("I could not find an appropriate accepted_hits.bam file. Failed to find: %s" \
                                                  % (bam_path))
            else:
                return bam_path 
        return bam_path

    def get_mask_file(self):
        option = self.prog_yargs['mask-file']
        if option == 'from_conditions':
            try:
                mask_path = self._conditions['mask_file']
                return mask_path
            except KeyError:
                return False
        else:
            return option

class CuffmergeCall(BaseCall):
    """
    Manage a single call to cuffmerge and store associated run data.
    """

    def __init__(self,yargs,email_info,run_id,run_log,run_err,conditions):

        self.prog_name = 'cuffmerge'

        BaseCall.__init__(self,yargs,email_info,run_id,run_log,run_err,conditions)

        self.prog_yargs = self.yargs.cuffmerge_options
        self.set_call_id()
        self.out_dir = self.get_out_dir()


        # set up options for program call
        self.opt_dict = self.init_opt_dict()
        self.opt_dict['o'] = self.out_dir
        self.opt_dict['ref-gtf'] = self.get_gtf_anno()
        self.opt_dict['ref-sequence'] = self.get_genome()
        self.construct_options_list()

        # now the positional args
        assembly_list = self.get_cufflinks_gtfs()

        # combine and save arg_str
        self.options_list.extend([assembly_list])
        self.arg_str = ' '.join(self.options_list)

    def get_out_dir(self):
        option = self.prog_yargs.o
        if option == 'from_conditions':
            return self.build_out_dir_path()
        else:
            return option

    def get_gtf_anno(self):
        option = self.prog_yargs['ref-gtf']
        if option == 'from_conditions':
            # Make sure all conditions agree on anno.gtf
            gtf_path = set([c['gtf_annotation'] for c in self._conditions])
            if len(gtf_path) == 1:
                gtf_path = gtf_path.pop()
            else:
                raise errors.InvalidFileFormatError('CHECK YAML CONFIG FILE: Conditions in group %s do not agree on which "ref-gtf" to use: %s.' \
                                                    % (self.group_id,gtf_path))
            return gtf_path
        else:
            return option

    def get_genome(self):
        option = self.prog_yargs['ref-sequence']
        if option == 'from_conditions':
            # Make sure all conditions agree on their genome seq
            genome_path = set([c['genome_seq'] for c in self._conditions])
            if len(genome_path) == 1:
                genome_path = genome_path.pop()
            else:
                raise errors.InvalidFileFormatError('CHECK YAML CONFIG FILE: Conditions in group %s do not agree on which "ref-sequence" to use: %s.' \
                                                    % (self.group_id,genome_path))
            return genome_path
        else:
            return option

    def get_cufflinks_gtfs(self):
        option = self.prog_yargs.positional_args.assembly_list
        if option == 'from_conditions':
            paths = []
            for condition in self._conditions:
                gtf_path = self.get_cuffGTF_path(condition)
                paths.append(gtf_path)
            assembly_list_file = open("%s/assembly_list.txt" % (self.out_dir.rstrip('/')),'w')
            assembly_list_file.write("\n".join(paths))
            assembly_list_file.close()
            return os.path.abspath(assembly_list_file.name)
        else:
            return option

    def get_cuffGTF_path(self,condition):
        cl_call_id = "cufflinks_%s" % (condition['name'])
        try:
            cl_call = self.yargs.call_records[cl_call_id]
            cl_out_dir = cl_call.out_dir
            gtf_path = "%s/transcripts.gtf" % (cl_out_dir.rstrip('/'))
        except (KeyError,AttributeError) as exp:
            msg = "WARNING: unable to find matching cufflinks call record in memory for condition: %s\nAttempting to find corresponding cufflinks outfile in your base_dir." \
                % (condition['name'])
            self.log_msg(err_msg=msg)

            # try to guess correct cufflinks out directory
            base_dir = self.yargs.run_options.base_dir
            gtf_path = "%s/%s/" % (base_dir.rstrip('/'),cl_call_id)
            if not os.path.exists(gtf_path):
                # TODO: build framework to handle this non-fatally
                raise errors.MissingArgumentError("I could not find an appropriate transcripts.gtf file. Failed to find: %s" \
                                                  % (gtf_path))
            else:
                return gtf_path
        return gtf_path