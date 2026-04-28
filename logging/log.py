import logging

# location libraries
import os 
import sys 
from pathlib import Path

logger = logging.getLogger(__name__)

'''
The below make is possible for the state.log file
to be created in the 'logging/' DIR
'''
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = Path(__file__).resolve().parent

# setting location for logs
logging.basicConfig(filename=os.path.join(BASE_DIR, 'state.log'),
                    encoding='utf-8',
                    # filemode= 'w',
                    level=logging.DEBUG)

# fucntions for causal code logging around the codebase
class logs: 
    # warning log
    def w_log(message) -> str:
        print('warning logged')
        return logger.warning(message)

    # error log
    def e_log(message) -> str:
        print('error logged')
        return logger.error(message)

    # info log
    def i_log(message) -> str:
        print('info logged')
        return logger.info(message)

    # debug log
    def d_log(message) -> str:
        print('debug logged')
        return logger.debug(message)