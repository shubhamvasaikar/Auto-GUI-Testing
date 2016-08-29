import logging
import logging.config

formatter = "%(asctime)s - %(levelname)-6s: %(name)s: %(message)s"
logging.basicConfig(filename="autotest.log", format=formatter, level=logging.NOTSET)
logging.getLogger(__name__)
