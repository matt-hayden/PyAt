from collections import namedtuple
import string
import subprocess
import sys

from . import AT, BATCH
from . import debug, info, warning, error, panic


QUEUES = '='+string.ascii_lowercase+string.ascii_uppercase


def job_key(job):
	return job.begins, job.queue


class Job(namedtuple('Job', 'jid begins queue owner')):
	def get_script(self, command=[AT, '-c'], encoding='UTF-8'):
		# with redirect_stdout...
		proc = subprocess.Popen(command+[str(self.jid)], stdout=subprocess.PIPE)
		out, _ = proc.communicate()
		return out.decode(encoding).splitlines()
	if sys.platform.startswith('linux'):
		@staticmethod
		def from_line(line):
			jid, line = line.split('\t', 1)
			begins = line[:24]
			try:
				begins = dateutil.parser.parse(begins)
			except:
				debug("{} left as string".format(begins))
			queue = QUEUES.index(line[25])
			owner = line[27:].strip()
			return Job(int(jid), begins, queue, owner)
	elif sys.platform.startwith('darwin'):
		@staticmethod
		def from_line(line):
			jid, line = line.split('\t', 1)
			try:
				begins = dateutil.parser.parse(line)
			except:
				debug("{} left as string".format(begins))
				begins = line.strip()
			return Job(int(jid), begins, None, None)
	def __repr__(self):
		return "{:8d} {:>24} {:02d} {:<}".format(*self)


def _get_jobs(command=[AT, '-l'], encoding='UTF-8'):
	# with redirect_stdout...
	proc = subprocess.Popen(command, stdout=subprocess.PIPE)
	out, _ = proc.communicate()
	for line in out.decode(encoding).splitlines():
		yield Job.from_line(line)


def print_jobs(jobs=None):
	if not jobs:
		jobs = sorted(_get_jobs(), key=job_key)
	#print("{:^8} {:^24} {:^2} {:<}".format(*'jid begins qn owner'.split()) )
	print('='*8, '='*24, '='*2, '='*8)
	for job in jobs:
		print(job)


jobs = sorted(_get_jobs(), key=job_key)
