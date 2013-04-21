#*****************************************************************************
#  encode_mail_li_file.py (part of the blacktie package)
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
######################
encode_mail_li_file.py
######################
Script to encode your email log in pswrd so that it will be obscured to MOST BUT NOT ALL people.
"""
import argparse
import sys
import base64


import blacktie


def main():
    """
    The main loop.  Lets ROCK!
    """

    desc = """This script takes a path to a file where you have placed your password for
    the email you want blacktie to use as the "sender" in its notification emails. It will
    replace the file with one containing your password once it has encoded it out of human
    readable plain-text into seemingly meaningless text. **THIS IS NOT FOOLPROOF:** If someone
    knows exactly what to look for they might figure it out. ALWAYS use good password
    practices and never use the same password for multiple important accounts!"""

    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--version', action='version', version='%(prog)s ' + blacktie.__version__,
                        help="""Print version number.""")
    parser.add_argument('input_file', type=str,
                        help="""Path to a file where you have placed your password for the email
                        you want blacktie to use as the "sender" in its notification emails.""")

    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)

    args = parser.parse_args()
    
    pswrd = ''.join([x.rstrip('\n') for x in open(args.input_file,'rU').readlines()])
    drwsp = base64.b64encode(pswrd)

    out_file = open(args.input_file,'w')
    out_file.write(drwsp)
    out_file.close()
    

if __name__ == "__main__":
    main()