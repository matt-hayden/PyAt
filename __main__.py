"""Simple Pythonic wrapper around the at and batch commands
Usage:
  py atgrep GREP_ARGS
  py atq

"""

import sys

import docopt

from . import *
from .tools import atgrep

print(sys.argv)
kwargs = docopt.docopt(__doc__, '0.2')
if kwargs['atgrep']:
	atgrep(kwargs.pop('GREP_ARGS'))
elif kwargs['atq']:
	print_jobs()
