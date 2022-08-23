import multiprocessing
import logging
from multiprocessing import shared_memory
import threading
from worker import job


def check_changes_in_shared_memory(sh_m):
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO,
                        filemode='w+', filename='./logs/shared_memory.txt')
    tmp = sh_m
    while True:
        if tmp != sh_m:
            logging.info(f'🔥 changes in shared memory')
            tmp = sh_m


def main():
    processes = []
    # create share memory
    sh_m = shared_memory.ShareableList(["0" for _ in range(1000)])
    # create 10 processes
    try:
        for number in range(10):
            pro = multiprocessing.Process(
                target=job, args=(sh_m.shm.name, number))
            processes.append(pro)
            pro.start()
    except KeyboardInterrupt:
        sh_m.s.close()
        sh_m.unlink()
        del sh_m
    # create thread to check changes in shared memory
    threading.Thread(target=check_changes_in_shared_memory,
                     args=(sh_m,)).start()

    return processes


if __name__ == '__main__':
    # logging.basicConfig(filename='main.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

    logging.info('🚀 starting ...')
    main()
