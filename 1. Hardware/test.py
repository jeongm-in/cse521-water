import threading
import time

def p(data):
    data.append('h')
    print(data)

data = []
t1 = threading.Timer(1, p, args=(data,))
t1.start()

time.sleep(10)


