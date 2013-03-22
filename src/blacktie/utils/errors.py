#*****************************************************************************
#  errors.py (part of the blacktie package)
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
errors.py
####################
Code defining custom base error classes to provide a foundation for graceful error handling.
"""
import warnings

class BlacktieError(StandardError):
    """Base class for exceptions in the blacktie package."""
    pass




class SystemCallError(BlacktieError):
    """Error raised when a problem occurs while attempting to run an external system call.

    Attributes:
        | ``errno`` -- return code from system call
        | ``filename`` -- file in volved if any
        | ``strerror`` -- error msg """
    
    def __init__(self,errno,strerror,filename=None):
        self.errno = errno
        self.strerror = strerror
        self.filename = filename
        
    def __str__(self):
        if not self.filename: 
            return """ERROR:\n %s.\nRETURN_STATE: %s.""" % (self.strerror.strip('\n'),
                                                          self.errno)
        else: 
            return """ERROR in %s:\n %s.\nRETURN_STATE: %s.""" % (self.filename,
                                                                self.strerror.strip('\n'),
                                                                self.errno)


class SanityCheckError(BlacktieError):
    """When a 'state check' comes back as conflicting or nonsensical."""
    pass

class UnexpectedValueError(BlacktieError):
    """When values that "should" not be possible happen; like if a variable was changed unexpectedly."""
    pass

class InvalidFileFormatError(BlacktieError):
    """When errors occur due to malformed file formats."""
    pass

class MissingArgumentError(BlacktieError):
    """When a required argument is missing from the parsed command line options."""
    def __init__(self,errMsg):
        self.msg = errMsg
    def __str__(self):
        return """ERROR: %s""" % (self.msg)

class InvalidOptionError(BlacktieError):
    def __init__(self,optVal,optName,validVals=None):
        self.optVal    = optVal
        self.optName   = optName
        self.validVals = validVals
        
    def __str__(self):
        if self.validVals:
            return """ERROR: %s is not a valid value for arg:%s.\n\tValid values are: %s""" % (self.optVal,self.optName,self.validVals)
        else:
            return """ERROR: %s is not a valid value for arg:%s.""" % (self.optVal,self.optName)




    
    

    