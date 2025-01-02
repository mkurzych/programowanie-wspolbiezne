import errno
import time
import os

uniq = int(time.time())
file = "plik" + str(uniq) + ".txt"

while True:
    try:
        fd = os.open("lockfile", os.O_CREAT|os.O_EXCL|os.O_RDWR)
        break
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        print("Serwer zajęty")
        time.sleep(0.25)

with open("bufor.txt", "w") as f:
    f.write(file + '\n')
    print("Podaj tekst, EOF by przestać")
    while True:
        line = input()
        f.write(line + '\n')
        if line == 'EOF':
            break

os.close(fd)

time.sleep(2)

while True:
    with open(file, "r") as f:
        r = f.read()
        if r != "":
            print(r)
            break
        time.sleep(0.25)

