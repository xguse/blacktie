Project Summary
===============

I want to collaborate with you!
-------------------------------
Contact me at wadunn83@gmail.com if you are a Python coder and want to or already have made improvements on this code.


Introducing Blacktie: a simpler way to do RNA-seq using Tophat, Cufflinks, and CummeRbund
---------------------------------------------------------------------------------------------
Leveraging multiple fastQ files full of RNA-seq reads into a coherent picture of gene expression and transcript models is a multi-step process.  It requires the organization and coordination of many files of different types through many different program calls and output steps.  Each step might take hours or days depending on your input data.  Then, as you are writing up your work, sometimes weeks/months later, you see that a new version of the programs you use has come out. Do you need to re-run your analysis?  What settings DID you use back then?

The Tophat/Cufflinks/CummeRbund group of programs makes quality RNA-seq analysis doable once you understand the process.  But what about when its time for you to leave the lab and you need to “train” someone else to repeat your process?  It can be a nightmare.  Especially if the trainee is not yet comfortable with the command line.

This is why I wrote the Blacktie pipeline software.  Its goals are to streamline and simplify the complex task of analyzing full RNA-seq experiments using these programs; to automatically record settings used and program output messages in a way that users can track them to data later; provide a base set of functions and classes that will allow users to create custom pipelines easily by editing a single file (or if they want: writing their own custom scripts).

Some of Blacktie’s features include:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- simple installation
- simple command line interface that allows almost ANYBODY to fully automate and reliably repeat their analysis of RNA-seq data with Tophat/Cufflinks/CummeRbund
- send email updates to the user
- intelligently continue with the analysis if a single run fails
- run multiple, complex tophat/cufflinks experiments at once using a single command
- generates SGE qsub-able scripts for use with a computing cluster
- checks for R installation
- checks for cummeRbund library and walks user through installation if its not installed yet
- automatic preliminary CummeRbund Quality Control, Basic Differential Expression, and Basic Pattern Discovery plots using CummeRbund

Dedicated bioinformatics personnel can be few and far between.  Blacktie aims to bring automated, reproducible RNA-seq with built-in record keeping to more labs so that your valuable data does not fester on your servers, and you can publish sooner.

Getting the code
----------------------
The code is available from the `Python Package Index <https://pypi.python.org/pypi>`_
or from its homepage:  https://github.com/xguse/blacktie

Visit :doc:`install` for more detailed instructions on getting and building the package.


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


