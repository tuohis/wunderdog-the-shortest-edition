import logging

DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING

def get_logger(name, level=WARNING, output_dir=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)
     
    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(level)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

    # create error file handler and set level to error
    # handler = logging.FileHandler(os.path.join(output_dir, "error.log"),"w", encoding=None, delay="true")
    # handler.setLevel(logging.ERROR)
    # formatter = logging.Formatter("%(levelname)s - %(message)s")
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
 
    # create debug file handler and set level to debug
    # handler = logging.FileHandler(os.path.join(output_dir, "all.log"),"w")
    # handler.setLevel(logging.DEBUG)
    # formatter = logging.Formatter("%(levelname)s - %(message)s")
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)