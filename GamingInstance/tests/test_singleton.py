from threading import Thread, Lock
import sys
from queue import Queue

sys.path.append('../')

from gaming_instance.singleton import SingletonMeta

class Test(metaclass=SingletonMeta):
    s = 0

    def sum(self):
        self.s += 1

lock = Lock()
lista = []

def test_sum():
    test = Test()

    for _ in range(200000):
        test.sum()

t1 = Thread(target=test_sum)
# t2 = Thread(target=test_sum)

t1.start()
# t2.start()

t1.join()
# t2.join()

test = Test()
print(test.s)
