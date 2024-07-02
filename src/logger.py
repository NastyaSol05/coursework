import logging
import os

project_root = os.path.abspath(os.path.dirname(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(os.path.join(project_root, "my_log.log"), mode="w")
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s"))
logger.addHandler(file_handler)
