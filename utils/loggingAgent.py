'''
A simplest customized logger
Usage: 
from loggingAgent import logger

Author: Linxia GONG 巩琳霞 (linxiagong@gmail.com)
Date: 2020-11-24 10:44:50
LastEditors: Linxia GONG 巩琳霞
LastEditTime: 2020-12-14 15:07:40
'''

import os
import logging
from time import gmtime, strftime

logger = logging.getLogger('My_log')

# Set logging message format
FORMAT = "%(asctime)s[%(filename)15s:%(lineno)s - %(funcName)15s() ]%(levelname)s: %(message)s"
# Set log file path
log_time = strftime("%Y_%m_%d_%H_%M", gmtime())
if not os.path.exists('./log/'):
    os.makedirs('./log/')
log_file_name = './log/Log.'+log_time+'.log'
# Set logging level: ERROR/ INFO/ DEBUG
logging.basicConfig(format=FORMAT, filename=log_file_name, level=logging.DEBUG)


#########################################################################
# Define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s[%(filename)15s:%(lineno)s - %(funcName)20s() ]%(levelname)s: %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logger.addHandler(console)