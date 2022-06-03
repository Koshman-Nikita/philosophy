import logging
from random import uniform
import threading
import time

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] [%(threadName)s]: %(message)s')

logger = logging.getLogger(__name__)


class Chopstick:
    def __init__(self, idx):
        self.idx = idx
        self.lock = threading.Lock()

    def pickup(self):
        self.lock.acquire()

    def putdown(self):
        self.lock.release()

    def __repr__(self):
        return f'Chopstick {self.idx}'


class Philosopher:

    def __init__(self, idx, chopsticks):
        self.idx = idx
        self.chopsticks = chopsticks

    def requestChopsticks(self, chopsticksIndexes):
        for chopstick in chopsticksIndexes:
            logger.info(f'{self} requested {self.chopsticks[chopstick]}')
            self.chopsticks[chopstick].pickup()
            logger.info(f'{self} picked up {self.chopsticks[chopstick]}')

    def leaveChopsticks(self, chopstickIndexes):
        for chopstick in chopstickIndexes:
            logger.info(f'{self} put down {self.chopsticks[chopstick]}')
            self.chopsticks[chopstick].putdown()

    def eat(self):
        sleeptime = uniform(0, 1)
        logger.info(f'{self} thinking for {sleeptime} sec')
        time.sleep(sleeptime)
        logger.info(f'{self} wants to eat after thinking for {sleeptime} sec')
        left, right = self.idx, (self.idx - 1) % 5

        if self.idx % 2 == 0:
            self.requestChopsticks((right, left))
        else:
            self.requestChopsticks((left, right))

        sleeptime = uniform(0, 1)
        logger.info(f'{self} is eating, with {self.chopsticks[left]} and {self.chopsticks[right]}')
        time.sleep(sleeptime)
        logger.info(f'{self} finishes eating after {sleeptime} sec')

        if self.idx % 2 == 0:
            self.leaveChopsticks((left, right))
        else:
            self.leaveChopsticks((right, left))

    def __repr__(self):
        return f'Philosopher {self.idx}'


def main():
    chopsticks = [Chopstick(i) for i in range(5)]

    philosophers = [Philosopher(i, chopsticks) for i in range(5)]

    threads = []

    for philosopher in philosophers:
        thread = threading.Thread(target=philosopher.eat)
        threads.append(thread)

        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
