#*****************************************************************************
#  cummerbund.py (part of the blacktie package)
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
cummerbund.py
####################
Code defining functions to encapsulate cummeRbund functionalities.
"""

'''
Notes on what basic functions I want to inlude and what the default output should be:

readCufflinks


'''
import os
import sys
import argparse

try:
    from rpy2.robjects import r
    from rpy2.rinterface import RRuntimeError
except ImportError as ie:
    raise errors.BlacktieError('Unable to import required module: "rpy2".  Try installing it with "[sudo] pip install rpy2".')
except RuntimeError as rte:
    raise errors.BlacktieError('Importing required module "rpy2" failed because no R application could be found on your system. Try again after instaling R.')


import blacktie
from blacktie.utils import errors
from blacktie.utils.misc import Bunch
from blacktie.utils.externals import mkdirp
from blacktie.utils.externals import runExternalApp

def print_my_plots(r, rplots, out='', file_type='pdf'):
    """
    saves our plots to files named with the plotting method used.
    
    :param r:       pointer to the R instance
    :param rplots:  the ``Bunch`` object where we stored our plots
    :param out:  a base directory to add to our saved plots into
    :param file_type:  the type of output file to use, choices: ['pdf','jpeg','png','ps']
    """
    out = out.rstrip('/')
    
    mkdirp(out)
    
    for plot_id in rplots:
        file_path = "%s/%s.%s" % (out,plot_id,file_type)
        r.ggsave(filename=file_path,plot=rplots[plot_id])
        
def run_cummeRbund_install():
    """
    provides R install of cummeRbund and provides user with all R output and prompts.
    """
    r.source("http://bioconductor.org/biocLite.R")
    r.biocLite('cummeRbund')
    

def import_cummeRbund_library():
    """
    imports cummeRbund library [r.library('cummeRbund')] or asks to install it otherwise.
    """
    try:
        r.library('cummeRbund')
    
    except RRuntimeError as exc:
        if "there is no package called" in str(exc):
            
            print '\n\nIt looks like you have not installed "cummeRbund" yet.\nWould you like me to try to install it for you now?\n'
            print '(This will require an active internet connection)'
            
            while 1:
                install_cmrbnd = raw_input('y/n: ')
                if install_cmrbnd == ('y'):
                    print '\nOK, I am going to hand you off to the R install process. Answer any prompts it asks you, and I will see you on the other side.\n\n'
                    raw_input('Press "Enter" when ready...')
                    
                    run_cummeRbund_install()
                    
                    print '\nGreat.  Now lets try this again, and hopefully we will be good to go!\n\nSee you soon!'
                    exit(0)
                    
                elif install_cmrbnd == 'n':
                    print '\nThis script requires that cummeRbund be installed. Please install it manually and try again.\n\nGoodbye.'
                    exit(0)
                    
                else:
                    print "Please type only 'y' or 'n'."
        else:
            raise exc
    
    
def main():
    """
    The main loop.  Lets ROCK!
    """

    desc = """This script reads the files in a cuffdiff output directory into cummeRbund, generates some standard preliminary plots, and saves the output."""

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--version', action='version', version='%(prog)s ' + blacktie.__version__,
                        help="""Print version number.""")    
    parser.add_argument('--cuffdiff-dir', type=str,
                        help="""Path to a cuffdiff output directory.""")
    #parser.add_argument('--cummerbund-db', type=str,
                        #help="""Path to a pre-built cummeRbund 'cuffData.db'. (this is rarely specified directly; usually --cuffdiff-dir works fine)""")
    parser.add_argument('--gtf-path', type=str, default='NULL',
                        help="""Path to gtf file used in cuffdiff analysis. This will provide transcript model information.""")
    parser.add_argument('--genome', type=str, default='NULL',
                        help="""String indicating which genome build the .gtf annotations are for (e.g. 'hg19' or 'mm9').""")
    parser.add_argument('--out', type=str, 
                        help="""A base directory to add to our saved plots into.""")
    parser.add_argument('--file-type', type=str, choices=['pdf','jpeg','png','ps'], default='pdf',
                        help="""The type of output file to use when saving our plots. (default: %(default)s)""")
    

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()    
    

    # import the cummeRbund libray to the R workspace
    import_cummeRbund_library()
        
    
    # read in the cuffdiff data
    cuff = r.readCufflinks(dir=args.cuffdiff_dir, gtfFile=args.gtf_path, genome=args.genome)
    
    # Find out if we have replicates
    genes_rep_fpkm = r.repFpkm(r.genes(cuff))
    replicate_ids = set(genes_rep_fpkm[2])
    
    if len(replicate_ids) > 1:
        we_have_replicates = True
    else:
        we_have_replicates = False
    
    # Store my plots here
    rplots = Bunch()
    
    
    # dispersion plot
    rplots.dispersionPlot = r.dispersionPlot(r.genes(cuff))
    
    # SCV plots
    if we_have_replicates:
        rplots.fpkmSCVPlot_genes = r.fpkmSCVPlot(r.genes(cuff))
        rplots.fpkmSCVPlot_isoforms = r.fpkmSCVPlot(r.isoforms(cuff))
    else:
        pass
    
    # Density Plots
    rplots.csDensity = r.csDensity(r.genes(cuff))    
    
    if we_have_replicates:
        rplots.csDensity_reps = r.csDensity(r.genes(cuff),replicates='T')
    else:
        pass
    
    # Box Plots
    rplots.csBoxplot = r.csBoxplot(r.genes(cuff))    
    
    if we_have_replicates:
        rplots.csBoxplot_reps = r.csBoxplot(r.genes(cuff),replicates='T')
    else:
        pass
    
    # Scatter Matrix
    rplots.csScatterMatrix = r.csScatterMatrix(r.genes(cuff))
    
    
    
    # TODO: csDendro does not use ggplot2 it seems so ggsave() does not work. When issue is fixed, uncomment this.
##    # Dendrograms
##    rplots.csDendro = r.csDendro(r.genes(cuff))    
##    
##    if we_have_replicates:
##        rplots.csDendro_reps = r.csDendro(r.genes(cuff),replicates='T')
        
    # Volcano Matrix
    rplots.csVolcanoMatrix = r.csVolcanoMatrix(r.genes(cuff))
    
    # Sig Matrix
    rplots.sigMatrix = r.sigMatrix(cuff,level='genes',alpha=0.05)
    
    
    # get significant genes
    mySigGeneIds = r.getSig(cuff,alpha=0.05,level='genes')
    mySigGenes = r.getGenes(cuff,mySigGeneIds)
    print "Significant Genes: %s" % (len(mySigGeneIds))
    
    # Preliminary Clustering
    ic = r.csCluster(mySigGenes,k=20)
    rplots.csClusterPlot = r.csClusterPlot(ic)
    
    # print the plots
    print_my_plots(r, rplots, out=args.out, file_type=args.file_type)
    
if __name__ == "__main__":
    main()