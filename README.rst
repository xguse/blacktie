This file STILL requires editing
==========================

This package is still VERY raw and, while quite functional in many respects, not complete.
The tophat and cufflinks and cuffmerge steps have been written and passed preliminary functionality tests. 

**I seek collaboration and 
contributions to improve this tool.**  

PLEASE take it and run with it, but send me your progress!

Its goal is to **simplify the integration of all the
input/output streams of the tophat/cufflinks workflow** into a single yaml based config
file and automate as much of everything else as possible so that once the config file
is filled out, **the entire process of analysing a multi-condition RNA-seq experiment can
be run with a single command.**  

I have not had time to fill in ALL the doc strings but will continue to update them regularly.

(Current version of the docs can be found here: https://blacktie.readthedocs.org/)

If you want to use/contribute before the docs are complete, please contact me at 
wadunn83@gmail.com for guidance.

Usage
-----
::

  usage: blacktie_pipeline.py [-h]
                              [--prog {tophat,cufflinks,cuffmerge,cuffdiff,all}]
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

::


Credits
-------

- `Distribute`_
- `Buildout`_
- `modern-package-template`_

.. _Buildout: http://www.buildout.org/
.. _Distribute: http://pypi.python.org/pypi/distribute
.. _`modern-package-template`: http://pypi.python.org/pypi/modern-package-template
