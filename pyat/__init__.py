
import sys

import logging
logger = logging.getLogger('' if __name__ == '__main__' else __name__)
logger.setLevel(logging.DEBUG if __debug__ else logging.WARNING)
debug, info, warning, error, fatal = logger.debug, logger.info, logger.warning, logger.error, logger.critical
__all__ = 'debug info warning error panic'.split()


if sys.platform.startswith('win'):
	AT='AT.EXE'
	BATCH='BATCH.EXE'
else:
	AT='at'
	BATCH='batch'
__all__ += ['AT', 'BATCH']

