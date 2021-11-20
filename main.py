import threading
import time
import sys

# Ref https://stackoverflow.com/a/32695845/885983
# - Updated to python3
# - Added Ctrl + c exit handler

c = threading.Condition()
flag = 0  # shared between Thread_A and Thread_B
val = 20
shouldExit = False


class Thread_A(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global flag
        global val  # made global here
        global shouldExit
        while shouldExit is False:
            c.acquire()
            if flag == 0:
                print(f"A: val={val}")
                time.sleep(0.1)
                flag = 1
                val = 30
                c.notify_all()
            else:
                c.wait()
            c.release()


class Thread_B(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        global flag
        global val  # made global here
        global shouldExit
        while shouldExit is False:
            c.acquire()
            if flag == 1:
                print(f"B: val={val}")
                time.sleep(0.5)
                flag = 0
                val = 20
                c.notify_all()
            else:
                c.wait()
            c.release()


if __name__ == "__main__":
    try:
        a = Thread_A("myThread_name_A")
        b = Thread_B("myThread_name_B")

        b.start()
        a.start()

        a.join()
        b.join()
    except KeyboardInterrupt:
        shouldExit = True
        print("\nexiting...")
        sys.exit(0)
