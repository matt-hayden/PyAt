
from contextlib import redirect_stdout
from datetime import datetime
import os
import re
import selectors
import subprocess
import sys


from . import debug, info, warning, error, fatal
from . import AT, BATCH
from .jobs import Job, get_queue
from .tools import search


def submit(syntax,
		   queue=None,
		   begins=None,
		   at_encoding='UTF-8'):
	"""
	syntax is a list of lines
	"""
	def _parse_output(lines, job_pattern=re.compile('\s*'.join(['job', '(\d+)', 'at', '(.*)']), re.IGNORECASE) ):
		for line in lines:
			if line.upper().startswith('WARNING:'):
				warning(line[9:].strip())
				continue
			m = job_pattern.match(line)
			if m:
				g = m.groups()
				return Job(int(g[0]), g[1].strip(), queue or 0, None)
	queue = get_queue(queue)
	if queue:
		command = [ AT, '-q', queue ]
		if isinstance(begins, (date, datetime)) and (datetime.now() < begins):
			command += [ '-t', begins.strftime('%Y%m%d%H%M.%S') ]
		else:
			command += [ 'now' ]
	else:
		command = [ BATCH ]
	debug(command)
	proc = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	_, out = proc.communicate(syntax.encode(at_encoding)) # all output is mushed through stderr :/
	return _parse_output(out.decode().splitlines())


def atgrep(*args, **kwargs):
	return '\n'.join(search(grep_args=args or sys.argv[1:], **kwargs))


def batch(sel=selectors.DefaultSelector(), timeout=None):
#	if os.isatty(0):
#		print("Emulating batch")
	sel.register(sys.stdin, selectors.EVENT_READ)
	for key, mask in sel.select(timeout):
		print( submit(key.fileobj.read()) )
