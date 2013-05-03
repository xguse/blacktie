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

import rpy2

import blacktie
from blacktie.utils.misc import Bunch


def print_my_plots(r, rplots, prefix='', file_type='pdf'):
    """
    saves our plots to files named with the plotting method used.
    
    :param r:       pointer to the R instance
    :param rplots:  the ``Bunch`` object where we stored our plots
    :param prefix:  a base path to add to our saved plots
    :param file_type:  the type of output file to use, choices: ['pdf','jpeg','png','ps']
    """
    prefix = prefix.rstrip('/')
    
    for plot_id in rplots:
        file_path = "%s/%s.%s" % (prefix,plot_id,file_type)
        r.ggsave(filename=file_path,plot=rplots[plot_id])
        

    
def main(cuffdiff_dir,cummerbund_db,gtf_path,genome,prefix,file_type):
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
    parser.add_argument('--prefix', type=str, 
                        help="""A base path to add to our saved plots.""")
    parser.add_argument('--file-type', type=str, choices=['pdf','jpeg','png','ps'], default='pdf',
                        help="""The type of output file to use when saving our plots. (default: %(default)s)""")
    

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()    
    
    

    # store R instance for easy access to the workspace
    r = rpy2.robjects.r
    
    # import cummeRbund library
    r.library('cummeRbund')
    
    # Find out if we have replicates
    genes_rep_fpkm = r.repFpkm(r.genes(cuff))
    replicate_ids = set(genes_rep_fpkm[2])
    
    if len(replicate_ids) > 1:
        we_have_replicates = True
    else:
        we_have_replicates = False
    
    # Store My Plots
    rplots = Bunch()
    
    # read in the cuffdiff data
    cuff = r.readCufflinks(dir=args.cuffdiff_dir, gtfFile=args.gtf_path, genome=args.genome)
    
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
        
    # Box Plots
    rplots.csBoxplots = r.csBoxplots(r.genes(cuff))    
    
    if we_have_replicates:
        rplots.csBoxplots_reps = r.csBoxplots(r.genes(cuff),replicates='T')
    
    # Scatter Matrix
    rplots.csScatterMatrix = r.csScatterMatrix(r.genes(cuff))
    
    
    # Dendrograms
    rplots.csDendro = r.csDendro(r.genes(cuff))    
    
    if we_have_replicates:
        rplots.csDendro_reps = r.csDendro(r.genes(cuff),replicates='T')
        
    # Volcano Matrix
    rplots.csVolcanoMatrix = r.csVolcanoMatrix(r.genes(cuff))
    
    # Sig Matrix
    rplots.sigMatrix = r.sigMatrix(cuff,level='genes',alpha=0.05)
    
    
    # get significant genes
    mySigGeneIds = r.getSig(cuff,alpha=0.05,level='genes')
    mySigGenes = r.getGenes(mySigGeneIds)
    print "Significant Genes: %s" % (len(mySigGeneIds))
    
    # Preliminary Clustering
    ic = r.csCluster(mySigGenes,k=20)
    rplots.csClusterPlot = r.csClusterPlot(ic)
    
    # print the plots
    print_my_plots(r, rplots, prefix='', file_type='pdf')