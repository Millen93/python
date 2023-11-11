import os, sys , time


ttlParent = 1000
for i in range(0, 10):
    pid_1 = os.fork()
    print("I wanna eat u brain!!!")
    if pid_1 == 0:
        sys.exit();

time.sleep(ttlParent);
os.wait()
