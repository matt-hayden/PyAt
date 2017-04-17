
from contextlib import redirect_stdout
from datetime import datetime, date, time
#import io
import re
import subprocess


from . import AT, BATCH
from .jobs import Job, QUEUES


def submit(syntax,
		   queue=None,
		   begins=None,
		   encoding='UTF-8'): # , s=io.StringIO()):
	"""If syntax is a list of tokens, they're safely quoted for shell
digestion.
Should you need to dispatch multi-line syntax, you're better off joining it
yourself into one string"""
	if isinstance(syntax, (tuple, list)):
		syntax=sq(syntax)
	def _parse_output(lines, job_pattern=re.compile('\s*'.join(['job', '(\d+)', 'at', '(.*)']), re.IGNORECASE) ):
		for line in lines:
			if line.upper().startswith('WARNING:'):
				warning(line[9:].strip())
				continue
			m = job_pattern.match(line)
			if m:
				g = m.groups()
				return Job(int(g[0]), g[1].strip(), queue or 0, None)
	if isinstance(queue, int):
		queue = QUEUES[queue]
	if queue:
		command = [ AT, '-q', queue ]
		if isinstance(begins, (date, datetime)) and (datetime.now() < begins):
			command += [ '-t', begins.strftime('%Y%m%d%H%M.%S') ]
		else:
			command += [ 'now' ]
	else:
		command = [ BATCH ]
	## Python 3.5
	#sp = s.tell()
	#with redirect_stderr(s) as out:
	#	proc = subprocess.Popen(command, stdin=subprocess.PIPE)
	#	proc.communicate(syntax.encode(encoding))
	#se = s.tell()
	#lines = s.read().splitlines()
	debug(command)
	proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	_, out = proc.communicate(syntax.encode(encoding)) # all output is mushed through stderr :/
	return _parse_output(out.decode(encoding).splitlines())

def batch(quiet=False):
	import os
	import sys
	if os.isatty(0) and not quiet:
		print("Emulating batch")
	submit(sys.stdin.read())
