
import subprocess
import sys

from . import debug, info, warning, error, fatal
from . import AT, BATCH
from .jobs import _get_jobs


if sys.platform.startswith('win'):
	GREP='GREP.EXE'
else:
	GREP='grep'

def search(grep_args, at_encoding='UTF-8'):
	for job in _get_jobs():
		jid, started, queue, owner = job
		label = str(jid)
		proc = subprocess.Popen([GREP, '--label='+label, '-H']+grep_args,
								stdin=subprocess.PIPE,
								stdout=subprocess.PIPE)
		contents = '\n'.join(job.get_script())
		out, _ = proc.communicate(contents.encode(at_encoding))
		if out:
			yield from out.decode().splitlines()
