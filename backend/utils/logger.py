import logging
import os
from utils.singleton import Singleton

class Logger(metaclass=Singleton):
    def __init__(self, logger_name, filename):
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter('%(asctime)s ~ %(name)s ~ %(levelname)s ~ %(message)s')
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(logging.INFO)
        self.logger.addHandler(sh)  
 
        fh = logging.FileHandler(filename)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger