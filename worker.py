"""
version 1.2.0

"""

import logging
import time
import random
from multiprocessing import shared_memory
from datetime import datetime


def heavy_computational_function(s: str) -> str:
    """my heavy computational function

    note: out put must be 8 byte
    """
    # TODO: Build a constant value every 30 seconds for a specific input

    time.sleep(0.02)
    now = datetime.now()
    if now.second <= 29:
        return f"X{s}"

    return f"O{s}"


def job(shm_name, pk):
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.INFO, filename=f'./logs/jobs{pk}.txt', filemode='w+')

    logging.info(f'🔥 job by id {pk} starting ...')
    # TODO: use defaultdict for cache
    cache = dict()
    # TODO: in this place we can find best value for cache in process when process in running
    # calculate all cache
    x = random.randint(1, 900)
    for item in range(x, x+101):
        cache[str(item)] = None

    logging.info(f"local cache: {cache}")
    while True:
        time.sleep(0.02)
        request = str(random.randint(1, 1000))
        logging.info(f"📩 request ==> {request} received")
        if request in cache.keys():
            if cache[request] is not None and time.time() - float(cache[request][0]) < 30:
                # search in local cache
                logging.info(f'🔥 returning cached result for {request}')
                print(cache[request][1])
            else:
                # update local cache
                # TODO: update the shared memory for best performance(mabye)
                # TODO: in this update we can use multithreading to speed up the process
                x = heavy_computational_function(request)
                cache[request] = [str(time.time()).split('.')[0][-4:], x]
                print(x)
        else:
            # search in shared memory
            sh_m = shared_memory.ShareableList(name=shm_name)
            if sh_m[int(request)] == "0":
                logging.info(
                    f"update  shared memory for request: {request}")
                # calculate value and set to the shared memory cache
                x = heavy_computational_function(request)
                now = str(time.time()).split('.')[0][-3:]
                sh_m[int(request)] = f'{now}:{x}'
                print(x)
            else:
                if float(str(time.time()).split('.')[0][-3:]) - float(sh_m[int(request)].split(':')[0]) < 30:
                    logging.info(
                        f'✅ returning result from shared memory for {request}')
                    print(sh_m[int(request)].split(':')[1])
                else:

                    x = heavy_computational_function(request)
                    now = str(time.time()).split('.')[0][-3:]
                    sh_m[int(request)] = f'{now}:{x}'
                    print(x)
