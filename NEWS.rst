.. This is your project NEWS file which will contain the release notes.
.. Example: http://www.python.org/download/releases/2.6/NEWS.txt
.. The content of this file, along with README.rst, will appear in your
.. project's PyPI page.

News
====

0.2.1.2
-----------
*Release date: 2013-07-17*

* version number system adopted to conform to PEP386
* This is a hot fix to squash a bug described in github issue: https://github.com/xguse/blacktie/issues/10
    * **in short:** on a Mac ``pprocess`` complained "AttributeError: 'module' object has no attribute 'poll'" when trying to set up a queue.
    * the quick fix is to look for that exception and continue without ``pprocess`` if encountered to avoid the fatal exception.



0.2.1
---------
*Release date: 2013-05-15*

* git tag: 'v0.2.1'
* added new script named blacktie-cummerbund to run cummeRbund
* added new class in calls.py CummerbundCall to use blacktie-cummerbund script to add cummeRbund plots to blacktie script
* checks for R and rpy2 installations
* if cummeRbund R library not found, it walks you through installing it
* ``src/blacktie/utils/calls.py``: - fixed _flag_out_dir() so that if the outdir has not been created yet it gracefully moves on
* ``examples/blacktie_config_example.yaml``: - added cummerbund_options
* ``requirements.txt``: - added rpy2
* updated docs

0.2.0rc1
--------

*Release date: 2013-04-19*

* git tag: 'v0.2.0rc1'
* Added support for handling biological replicates in cuffdiff runs.
* Major changes to yaml config:
    * condition_queue[index].group_id --> condition_queue[index].experiment_id
    * addition of condition_queue[index].replicate_id to track replicate data
    * condition_queue[index].name now represents description of an 'experiemental condition' and will be shared by replicates.


0.1.1
-----

*Release date: 2013-03-21*

* git commit SHA digest: 9d7c02d5e7f4ec8970bb2291c3eb6ff8f4dbe542
* git tag: 'v0.1.1'


0.1_dev
-------

*Release date: 2013-03-20*

* git commit SHA digest: 808c11fb396c71af55ff690fa6f2e628e5ffd758
* git tag: 'v0.1-dev'
* First uploaded to PyPI
* This verion is still under active development.

