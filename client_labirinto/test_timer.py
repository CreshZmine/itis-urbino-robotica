import timer
import time
t = timer.Timer()
t.start()
time.sleep(2)
t.start()
print t.read()
time.sleep(2)
print t.stop()
