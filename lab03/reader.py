import sys
import os

first_file = sys.argv[1]
first_word = sys.argv[2].lower()

parent = os.getpid()


def read_next(file, word):
    count = 0
    wait = 0
    with open(file, "r") as f:
        d = f.readlines()
        for line in d:
            for w in line.split():
                if "\\input" in w:
                    pid = os.fork()
                    if pid == 0:
                        read_next(w[7:-1], word)
                    else:
                        wait += 1
                if w.lower() == word:
                    count += 1
        while wait != 0:
            status = os.wait()
            count += os.WEXITSTATUS(status[1])
            wait -= 1
    if parent == os.getpid():
        print("Count:", count)
    exit(count)


read_next(first_file, first_word)
