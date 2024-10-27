import time
import os

while True:
    with open("bufor.txt", "r+") as bufor:
        b = bufor.readlines()
        if b:
            with open(b[0][:-1], "w") as f:
                f.write("Message received")
                with open("bufor.txt", 'w'): pass
            try:
                os.unlink("lockfile")
            except FileNotFoundError:
                pass
        time.sleep(0.25)
