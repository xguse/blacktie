Getting started
===============
.. Note:: Make sure that you have successfully installed the blacktie module before trying the activities below.

To test whether your installation was successful, open a new terminal session and type the following command. ::

  $ blacktie

You should see the help text for blacktie and it should look something like this:

.. code-block:: none
  
  $ blacktie -h
  
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

The --prog option
---------------------
This tells ``blacktie`` which part of the pipeline you would like to run.  Any part can be run individually as long as the correct files exist.  You can also run the whole thing from ``tophat`` to ``cuffdiff`` in one fell swoop if you like!

The --hide-logs option
--------------------------
This names your log files so that they are hidden in "\*nix" systems.

The --modes option
----------------------
``blacktie`` can run in three modes.  The first, ``analyze``, actually runs the pipeline and does the analyses.  However, it can be useful to simply view what WOULD be done to make sure that ```blacktie`` is producing command line calls that match what you expected.  For this, use the ``dry_run`` mode. 

Further, if you are working on a compute cluster running something like a "Sun Grid Engine" (`SGE <http://en.wikipedia.org/wiki/Oracle_Grid_Engine>`_) to which you must `submit jobs <https://wikis.utexas.edu/display/CCBB/sge-tutorial>`_ using ``qsub``, it may not be a good idea to submit a job running all of ``blacktie`` as a single ``qsub`` job.  For this it can be helpful to have ``blacktie`` write all of your ``qsub`` scripts for you based on a template. Each bash script represents a single program call to the tophat/cufflinks suite.

.. Note:: A starter template for SGE submission can be found here: ``blacktie/examples/qsub.template``.  You will want to become familiar with how `Mako <http://www.makotemplates.org/>`_ processes templates if you plan to customize this much.

Here is what the starter template looks like:

.. literalinclude:: ../examples/qsub.template
   :language: bash
   :linenos:
  

The configuration file
----------------------
The configuration file is a `YAML-based <http://en.wikipedia.org/wiki/YAML>`_ document that is where we will store all of the complexity of the options, input and output files of the typical tophat/cufflinks workflow.  This way we have though about what we want to do with our RNA-seq data from start to finish before we actually start the analysis.  Also, this config file acts as a check on our poor memory.  If you get strange results you don't have to worry about whether you entered the samples backwards since you can go back to this config file and see exactly what files and settings were used.

.. Note:: If you are running blacktie in ``analyze`` mode, you will have many more files created that document every step of the process where the output files are actually placed as well as central log files.

Here is a dummy example of a config file:

.. Note:: A copy of this file can be found here: ``blacktie/examples/blacktie_config_example.yaml``


.. literalinclude:: ../examples/blacktie_config_example.yaml
   :language: yaml
   :linenos:


Using e-mail notifications
--------------------------
.. Note:: For now, only gmail addresses can be used to *send* notifications because the server settings are hardcoded into the functions right now.  I will soon add this info to the config file and then any smtp server will be usable.  *Any* email can be used as the recipient. 

.. warning:: Also: gmail's 2-step authentication will NOT work.  Sorry.  I will look into how to deal with that eventually.

You will need to provide your password in order to use the email notifications but it is not a good idea to store human readable passwords lying around your system.  So the file that is used to store your password must contain a version of your password that has been encoded in base64.  This will scramble your password beyond most people's ability to read it as a password as long as you don't name it something silly like ``password_file.txt``.   

The help text for ``blacktie-encode`` is:

.. code-block:: none

  $ blacktie-encode -h
  
  usage: blacktie-encode [-h] input_file

  This script takes a path to a file where you have placed your password for the
  email you want blacktie to use as the "sender" in its notification emails. It
  will replace the file with one containing your password once it has encoded it
  out of human readable plain-text into seemingly meaningless text. **THIS IS
  NOT FOOLPROOF:** If someone knows exactly what to look for they might figure
  it out. ALWAYS use good password practices and never use the same password for
  multiple important accounts!

  positional arguments:
    input_file  Path to a file where you have placed your password for the email
		you want blacktie to use as the "sender" in its notification
		emails.

  optional arguments:
    -h, --help  show this help message and exit



Tutorial
===============

A more detailed tutorial is under development, so *watch this space!*