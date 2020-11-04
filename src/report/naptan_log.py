import cons
import etl
import geos
import visualise
import report
import logging
from datetime import datetime

timestr = datetime.now().strftime("%Y_%m_%d")

# %%


def main():
    """[summary]

    Raises:
        ke: [description]
        e: [description]
        e: [description]

    Returns:
        [type]: [description]
    """

    # create logger with for open naptan.
    logger = logging.getLogger("Open_Naptan_Process")
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages.
    fh = logging.FileHandler(f"{timestr}_Open_Naptan.log")
    fh.setLevel(logging.DEBUG)
    fh.encoding('utf-8')
    return logger.addHandler(fh)


if __name__ == '__main__':
    main()
