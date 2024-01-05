from __future__ import print_function
import logging
import sys



logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

msg_fmt = logging.Formatter("%(asctime)-15s %(funcName)-20s"
                            "%(levelname)-8s %(message)s")

strhndl = logging.StreamHandler(sys.stdout)
strhndl.setFormatter(fmt=msg_fmt)

fhndl = logging.FileHandler(__file__ + ".log", mode='a')
fhndl.setFormatter(fmt=msg_fmt)

logger.addHandler(strhndl)
logger.addHandler(fhndl)

logger.info("information message")
logger.debug("debug message")


def function_one():
    logger.warning("warning message")


def function_two():
    logger.error("error message")


function_one()
function_two()
