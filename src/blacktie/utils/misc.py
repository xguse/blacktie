#*****************************************************************************
#  misc.py (part of the blacktie package)
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
misc.py
####################
Code facilitating random aspects of this package.
"""
import os
import sys
import inspect
import smtplib
import base64
import time
import re
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from collections import defaultdict


def get_version_number(path_to_setup):
    """
    Provides access to current version info contained in setup.py
    """
    
    setup_path = path_to_setup
    with open(setup_path, 'rb') as f:
        match = re.search(
            '\s*[\'"]?version[\'"]?\s*[=:]\s*[\'"]?([^\'",]+)[\'"]?',
            f.read().decode('utf-8'), re.I)

    if match:
        version_string = match.group(1)
        return version_string

    else:
        print("No version definition found in ", setup_path)


class Bunch(dict):
    """
    A dict like class to facilitate setting and access to tree-like data.  Allows access to dictionary keys through 'dot' notation: "yourDict.key = value".
    """
    def __init__(self, *args, **kwds):
        super(Bunch,self).__init__(*args,**kwds)
        self.__dict__ = self

def bunchify(dict_tree):
    """
    Traverses a dictionary tree and converts all sub-dictionaries to Bunch() objects.
    """
    for k,v in dict_tree.iteritems():
        if type(v) == type({}):
            dict_tree[k] = bunchify(dict_tree[k])
    return Bunch(dict_tree)


def whoami():
    """
    Returns the name of the currently active function.
    """
    return inspect.stack()[1][3]


def email_notification(sender,to,subject,txt,pw,server_info):
    """
    Sends email to recipient using GMAIL server by default but will now accept ``server_info`` to customize this.
    
    :param sender: email address of sender
    :param to: email addres of recipient
    :param subject: subject text
    :param txt: body text
    :param pw: password of ``sender``
    :param server_info: dictionary = {'host':``str``,'port':``int``}

    :returns: None
    
    .. todo:: **DONE** make ``email_notification()`` adjustable for other email servers
    """
    if sender:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(txt))
    
        host = server_info['host']
        port = server_info['port']
        server = smtplib.SMTP(host, port)
        
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
    else:
        pass
        
    
def get_time():
    """
    Return system time formatted as 'YYYY:MM:DD-hh:mm:ss'.
    """
    t = time.localtime()
    return time.strftime('%Y.%m.%d-%H:%M:%S',t)
        
    

def map_condition_groups(yargs):
    """
    creates a Bunch obj ``groups`` with key='experiment_id' from ``yargs``, value=list(condition_queue objects with 'experiment_id')
    
    :param yargs: argument object generated from the yaml config file
    :returns: ``groups``
    """
    groups = defaultdict(list)
    for condition in yargs.condition_queue:
        groups[condition['experiment_id']].append(condition)
    groups = Bunch(dict(groups))
    return groups

def uniques(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if x not in seen and not seen_add(x)]