Welcome to Blacktie!
==========================

This package is functional but under heavy development so you may want to periodically
pull the latest code from the repo at git://github.com/xguse/blacktie.git.

For the **LATEST** version pull the 'develop' branch.

**I seek collaboration and contributions to improve this tool.**  

**PLEASE** take it and run with it, but send me your progress!

Its goal is to **simplify the integration of all the
input/output streams of the tophat/cufflinks workflow** into a single yaml based config
file and automate as much of everything else as possible so that once the config file
is filled out, **the entire process of analysing a multi-condition RNA-seq experiment can
be run with a single command.**  

I have not had time to fill in ALL the doc strings but updating them regularly.

(Current version of the docs can be found here: http://xguse.github.com/blacktie/)

If you want to use/contribute before the docs are complete, please feel free to contact me at 
wadunn83@gmail.com for guidance.

Issue tracking
--------------
If you find issues, bugs, or have feature requests, please go here to submit them: https://github.com/xguse/blacktie/issues


Blacktie Poster
------------------------


.. raw:: html
	<iframe src="http://wl.figshare.com/articles/714149/embed?show_title=1" width="568" height="200" frameborder="0"></iframe>


To credit the use of blacktie please cite the poster using the DOI link provided.

	*Introducing Blacktie: a simpler way to do RNA-seq using Tophat/Cufflinks/CummeRbund*. Augustine Dunn. figshare.
	http://dx.doi.org/10.6084/m9.figshare.714149



Usage
-----
.. code-block:: none

	usage: blacktie [-h] [--version]
	                [--prog {tophat,cufflinks,cuffmerge,cuffdiff,cummerbund,all}]
	                [--hide-logs] [--no-email]
	                [--mode {analyze,dry_run,qsub_script}]
	                config_file

	This script reads options from a yaml formatted file and organizes the
	execution of tophat/cufflinks runs for multiple condition sets.

	positional arguments:
	  config_file           Path to a yaml formatted config file containing setup
	                        options for the runs.

	optional arguments:
	  -h, --help            show this help message and exit
	  --version             Print version number.
	  --prog {tophat,cufflinks,cuffmerge,cuffdiff,cummerbund,all}
	                        Which program do you want to run? (default: tophat)
	  --hide-logs           Make your log directories hidden to keep a tidy
	                        'looking' base directory. (default: False)
	  --no-email            Don't send email notifications. (default: False)
	  --mode {analyze,dry_run,qsub_script}
	                        1) 'analyze': run the analysis pipeline. 2) 'dry_run':
	                        walk through all steps that would be run and print out
	                        the command lines; however, do not send the commands
	                        to the system to be run. 3) 'qsub_script': generate
	                        bash scripts suitable to be sent to a compute
	                        cluster's SGE through the qsub command. (default:
	                        analyze)	





Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template


.. image:: https://d2weczhvl823v0.cloudfront.net/xguse/blacktie/trend.png
  :alt: Bitdeli badge
  :target: https://bitdeli.com/free
