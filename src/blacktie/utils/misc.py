#*****************************************************************************
#  misc.py (part of the blacktie package)
#
#  (c) 2013 - Augustine Dunn
#  James Laboratory
#  Department of Biochemistry and Molecular Biology
#  University of California Irvine
#  wadunn83@gmail.com
#
#  Licenced under the GNU General Public License 2.0 license.
#******************************************************************************

"""
####################
misc.py
####################
Code facilitating random aspects of this package.
"""

import sys
import inspect
import smtplib
import base64
import time
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText



class Bunch(dict):
    """
    A dict like class to facilitate setting and access to tree-like data.
    """
    def __init__(self, *args, **kwds):
        super(Bunch,self).__init__(*args,**kwds)
        self.__dict__ = self

def bunchify(dict_tree):
    """
    TODO: doc
    """
    for k,v in dict_tree.iteritems():
        if type(v) == type({}):
            dict_tree[k] = bunchify(dict_tree[k])
    return Bunch(dict_tree)


def whoami():
    """Returns the name of the currently active function."""
    return inspect.stack()[1][3]


def email_notification(sender,to,subject,txt,pw):
    """
    """
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(txt))
    
    server = smtplib.SMTP("smtp.gmail.com", 587)    
    
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(sender,pw)
        server.sendmail(sender,to,msg.as_string())
        server.close()
    except (smtplib.SMTPAuthenticationError,
            smtplib.SMTPConnectError,
            smtplib.SMTPDataError,
            smtplib.SMTPException,
            smtplib.SMTPHeloError,
            smtplib.SMTPRecipientsRefused,
            smtplib.SMTPResponseException,
            smtplib.SMTPSenderRefused,
            smtplib.SMTPServerDisconnected) as e:
        
        sys.stderr.write("Warning: %s was caught while trying to send your mail.\nSubject:%s\n" % (e.__class__.__name__,subject))

        server.rset()
        
        
    
def get_time():
    """
    Return system time formatted as 'YYYY:MM:DD-hh:mm:ss'.
    """
    t = time.localtime()
    return "%s.%s.%s-%s:%s:%s" % (t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
        
    

    