from __future__ import print_function
import logging
import multiprocessing as mp
from random import randint
import sys
import time


def sleepy(seconds):
    proc_name = mp.current_process().name
    logger.info("{} is sleeping for {} seconds.".format(
        proc_name, seconds))
    time.sleep(seconds)


logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
msg_fmt = logging.Formatter("%(asctime)-15s %(funcName)-7s "
                            "%(levelname)-8s %(message)s")
strhndl = logging.StreamHandler(sys.stdout)
strhndl.setFormatter(fmt=msg_fmt)
logger.addHandler(strhndl)

num_workers = 5
workers = []
for w in range(num_workers):
    p = mp.Process(target=sleepy, args=(randint(1, 20),))
    p.start()
    workers.append(p)

for worker in workers:
    worker.join()
    logger.info("Joined process {}".format(worker.name))
