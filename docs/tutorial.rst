Getting started
===============
.. Note:: Make sure that you have successfully installed the blacktie module before trying the activities below.

To test whether your installation was successful, open a new terminal session and type the following command. ::

  $ blacktie

You should see the help text for blacktie and it should look something like this:

.. code-block:: none
  
  usage: blacktie [-h] [--prog {tophat,cufflinks,cuffmerge,cuffdiff,all}]
		  [--hide-logs] [--mode {analyze,dry_run,qsub_script}]
		  config_file

  This script reads options from a yaml formatted file and organizes the
  execution of tophat/cufflinks runs for multiple condition sets.

  positional arguments:
    config_file           Path to a yaml formatted config file containing setup
			  options for the runs.

  optional arguments:
    -h, --help            show this help message and exit
    --prog {tophat,cufflinks,cuffmerge,cuffdiff,all}
			  Which program do you want to run? (default: tophat)
    --hide-logs           Make your log directories hidden to keep a tidy
			  'looking' base directory. (default: False)
    --mode {analyze,dry_run,qsub_script}
			  1) 'analyze': run the analysis pipeline. 2) 'dry_run':
			  walk through all steps that would be run and print out
			  the command lines; however, do not send the commands
			  to the system to be run. 3) 'qsub_script': generate
			  bash scripts suitable to be sent to a compute
			  cluster's SGE through the qsub command. (default:
			  analyze)

If this worked, great! Let's move on to what all that means.

The configuration file
----------------------
The configuration file is a `YAML-based <http://en.wikipedia.org/wiki/YAML>`_ document that is where we will store all of the complexity of the options, input and output files of the typical tophat/cufflinks workflow.  This way we have though about what we want to do with our RNA-seq data from start to finish before we actually start the analysis.  Also, this config file acts as a check on our poor memory.  If you get strange results you don't have to worry about whether you entered the samples backwards since you can go back to this config file and see exactly what files and settings were used.

.. Note:: If you are running blacktie in ``analyze`` mode, you will have many more files created that document every step of the process where the output files are actually placed as well as central log files.

Here is a dummy example of a config file:

.. code-block:: yaml
  :linenos:

  ---
  run_options:
    base_dir: /path/to/project/base_dir
    run_id: False     # if false; uses current date/time for uniqe run_id everytime
    bowtie_indexes_dir: /path/to/bowtie2_indexes
    email_info:
      sender: from_me@email.com
      to: to_you@email.com
      li: /path/to/file/containing/base64_encoded/login_info # base64_encoded pswrd for from_me@email.com

  tophat_options:
    o: from_conditions
    library-type: fr-unstranded
    p: 6
    r: 125
    mate-std-dev: 25
    G: from_conditions
    no-coverage-search: True
    positional_args:
      bowtie2_index: from_conditions
      left_reads: from_conditions
      right_reads: from_conditions
	
  cufflinks_options:
    o: from_conditions
    p: 7
    GTF-guide: from_conditions
    3-overhang-tolerance: 5000
    frag-bias-correct: from_conditions # if not False; path to genome fasta
    multi-read-correct: True
    upper-quartile-norm: True
    positional_args:
      accepted_hits: from_conditions

  cuffmerge_options:
    o: from_conditions # output directory
    ref-gtf: from_conditions
    p: 6
    ref-sequence: from_conditions
    positional_args:
      assembly_list: from_conditions # file with path to cufflinks gtf files to be merged

  cuffdiff_options:
    o: from_conditions
    labels: from_conditions
    p: 6
    time-series: True
    upper-quartile-norm: True
    frag-bias-correct: from_conditions
    multi-read-correct: True
    positional_args:
      transcripts_gtf: from_conditions
      sample_bams: from_conditions


  condition_queue:
    -
      name: control_1
      group_id: 0
      left_reads:
	- /path/to/control_1/techRep1.left_reads.fastq
	- /path/to/control_1/techRep2.left_reads.fastq
      right_reads:
	- /path/to/control_1/techRep1.right_reads.fastq
	- /path/to/control_1/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: treatment_1
      group_id: 0
      left_reads:
	- /path/to/treatment_1/techRep1.left_reads.fastq
	- /path/to/treatment_1/techRep2.left_reads.fastq
      right_reads:
	- /path/to/treatment_1/techRep1.right_reads.fastq
	- /path/to/treatment_1/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: control_2
      group_id: 1
      left_reads:
	- /path/to/control_2/techRep1.left_reads.fastq
	- /path/to/control_2/techRep2.left_reads.fastq
      right_reads:
	- /path/to/control_2/techRep1.right_reads.fastq
	- /path/to/control_2/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename

    -
      name: treatment_2
      group_id: 1
      left_reads:
	- /path/to/treatment_2/techRep1.left_reads.fastq
	- /path/to/treatment_2/techRep2.left_reads.fastq
      right_reads:
	- /path/to/treatment_2/techRep1.right_reads.fastq
	- /path/to/treatment_2/techRep2.right_reads.fastq
      genome_seq: /path/to/species/genome.fa
      gtf_annotation: /path/to/species/annotation.gtf
      bowtie2_index: species.bowtie2_index.basename
  ...

Using e-mail notifications
--------------------------
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.

Using different modes
---------------------
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.

Tutorial
===============

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque ipsum risus, scelerisque vitae consequat sit amet, placerat vitae turpis. Aliquam cursus justo vitae quam convallis vel auctor dui tristique. Nam justo nisl, pretium a scelerisque dictum, tincidunt sit amet diam. Donec neque nisi, ornare quis varius nec, scelerisque nec tellus. Maecenas neque purus, lobortis ac malesuada ut, vestibulum non dui. Proin tempor dolor est, quis facilisis orci. Maecenas varius dolor nec urna pellentesque adipiscing. Quisque mi lorem, fringilla non elementum quis, cursus sed nibh. Phasellus pellentesque turpis non enim interdum eget molestie purus interdum. Nunc id nunc justo, sit amet euismod velit.