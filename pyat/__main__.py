"""Simple Pythonic wrapper for at and batch.
Usage:
  asdf atgrep GREP_ARGS
  asdf atq
  asdf batch
  asdf shell (-c|-s)

"""
import os, os.path

import docopt

from . import *
from .cli import *

aliases = { 'atgrep': get_command_line(['atgrep']) }
kwargs = docopt.docopt(__doc__)

if kwargs['atgrep']:
	for line in atgrep(kwargs.pop('GREP_ARGS')):
		print(line)
elif kwargs['atq']:
	print_jobs()
elif kwargs['batch']:
	batch()
elif kwargs['shell']:
	if os.isatty(1):
		print('# These should sourced with eval `!!`') # same on bash, csh, zsh
	if kwargs['-c']:
		for a, c in aliases.items():
			print('alias {} {}'.format(a, sq(*c)) )
	else:
		for a, c in aliases.items():
			print('alias {}="{}"'.format(a, sq(*c)) )

