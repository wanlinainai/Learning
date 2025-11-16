# import subprocess
#
# print('$ nslookup www.python.org')
#
# r = subprocess.call(['nslookup', 'www.python.org'])
#
# print('Exit code:', r)


## 进程之间的 通信
from multiprocessing import Process, Queue
import os, time, random

def write(q):
    print(f'写进程{os.getpid()}')
    for value in ['A', 'B', 'C']:
        print(f'Put {value} to queue...')
        q.put(value)
        time.sleep(random.random())

def read(q):
    print(f'读进程{os.getpid()}')
    while True:
        # block=True，会一直等到队列中有数据，timeout是设置等待的时长，如果超过的报错
        value = q.get(True, timeout=2)
        print(f'Get {value} from queue')

if __name__ == '__main__':
    q= Queue()
    pw = Process(target=write, args=(q, ))
    pr = Process(target=read, args=(q, ))

    pw.start()

    pr.start()

    pw.join()

    pr.terminate()