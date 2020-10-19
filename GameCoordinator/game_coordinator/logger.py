import logging
import sys
import coloredlogs

coloredlogs.install()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger()