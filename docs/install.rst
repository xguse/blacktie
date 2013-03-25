Installation
============

Requirements
------------

The following python modules must be installed for blacktie to function properly: ::

  Mako>=0.7.3
  PyYAML>=3.10
    
The following modules will provide useful but optional functionality: ::

  pprocess>=0.5



Installing the latest version from the git repository
-----------------------------------------------------
.. Note:: Git is a **very** useful tool to have installed and to know how to use.  `Learn more here <http://git-scm.com/>`_ and `try it out here <http://try.github.com/>`_.

Clone the repo::
    
  $ git clone git://github.com/xguse/blacktie.git
    
Install with any unmet requirements using ``pip``: ::
  
  $ [sudo] pip install -r blacktie/requirements.txt blacktie

Install using standard ``setup.py`` script: ::
  
  $ cd blacktie
  $ [sudo] python setup.py install

Use ``pip`` to obtain the package from `PyPI <https://pypi.python.org/pypi>`_
------------------------------------------------------------------------------
::

  $ [sudo] pip install blacktie Mako PyYAML pprocess



Installing without using ``git`` or ``pip`` for the download
------------------------------------------------------------
After installing the requirements: ::

  $ wget https://github.com/xguse/blacktie/archive/master.zip
  $ unzip master.zip
  $ cd blacktie-master
  $ [sudo] python setup.py install

Test to see whether the install worked
--------------------------------------
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

If this worked, great! 


.. raw:: html
  <script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

    ga('create', 'UA-39589366-1', 'github.com');
    ga('send', 'pageview');

  </script>