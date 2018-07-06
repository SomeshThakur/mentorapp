import logging
import random
import threading
import time
import requests

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s', )

q = []


def consumer(cv):
    logging.debug('Consumer thread started ...')
    with cv:
        logging.debug('Consumer waiting ...')
        cv.wait()
        if q != []:
            item = q.pop()
            result = requests.get(url='')
        logging.debug('Consumer consumed the resource')


def producer(cv):
    logging.debug('Producer thread started ...')
    with cv:
        item = random.random(1, 10)
        q.append(item)
        logging.debug('Making resource available')
        logging.debug('Notifying to all consumers')
        cv.notifyAll()


if __name__ == '__main__':
    condition = threading.Condition()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition,))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition,))
    pd = threading.Thread(name='producer', target=producer, args=(condition,))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    pd.start()
