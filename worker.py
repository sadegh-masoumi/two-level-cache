"""
version 1.1.0

"""

import logging
import time
import random
import string
from multiprocessing import shared_memory


def heavy_computational_function(s: str) -> str:
    """my heavy computational function"""
    time.sleep(0.02)
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for _ in range(10))
    return result_str


def job(shm_name, pk):
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        level=logging.INFO, filename=f'./logs/jobs{pk}', filemode='w+')

    logging.info(f'🔥 job by id {pk} starting ...')
    cache = dict()
    x = random.randint(1, 901)
    for item in range(x, x+100):
        cache[str(item)] = [time.time(),
                            heavy_computational_function(f'{item}')]

    logging.info(f"local cache: {cache}")
    while True:
        time.sleep(0.02)
        request = str(random.randint(1, 1000))
        logging.info(f"📩 request ==> {request} received")
        if request in cache.keys():
            if time.time() - cache[request][0] < 30:
                # search in local cache
                logging.info(f'🔥 returning cached result for {request}')
                print(cache[request][1])
            else:
                # update local cache
                # TODO: update the shared memory for best performance(mabye)
                # TODO: in this update we can use multithreading to speed up the process
                x = heavy_computational_function(request)
                cache[request] = [time.time(), x]
                print(x)
        else:
            # search in shared memory
            sh_m = shared_memory.ShareableList(name=shm_name)
            for index, item in enumerate(sh_m):
                if item == "0":
                    continue
                t, value = item.split(':')
                if value == request:
                    if time.time() - float(t) < 30:
                        logging.info(
                            f'✅ returning result from shared memory for {request}')
                        print(value)
                        break
                    else:
                        # update cache memory
                        logging.info(
                            f"update cache memory for request:{request}")
                        logging.info(f"cache memory : {cache}")
                        x = heavy_computational_function(request)
                        sh_m[index] = f'{time.time()}:{x}'
                        print(x)
                        break
            # not in cache
            # find in and set to cache
            else:
                x = heavy_computational_function(request)
                logging.info(f"update  shared memory for request: {request}")
                logging.info(f"shared memory : {sh_m}")
                for item in enumerate(sh_m):
                    if item == "0":
                        sh_m[index] = f'{time.time()}:{x}'
