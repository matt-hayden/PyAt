"""Simple Pythonic wrapper for at and batch.
Usage:
  asdf atgrep GREP_ARGS
  asdf atq
  asdf batch

"""

import sys

import docopt

from . import *

kwargs = docopt.docopt(__doc__)
if kwargs['atgrep']:
	for line in atgrep(kwargs.pop('GREP_ARGS')):
		print(line)
elif kwargs['atq']:
	print_jobs()
elif kwargs['batch']:
	batch()
