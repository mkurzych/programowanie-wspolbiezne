import os
import errno
import time

uniq = int(time.time())

C_FIFO = 'klient' + str(uniq)
FIFO = 'kolejka'
len_fifo = len(C_FIFO)

try:
    os.mkfifo(C_FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise


person = input("Podaj id: ")
if int(person) < 10:
    person = "0" + person


fifo_out = os.open(FIFO, os.O_WRONLY)
os.write(fifo_out, (str(len_fifo) + person + C_FIFO).encode())

fifo_in = os.open(C_FIFO, os.O_RDONLY)

r = os.read(fifo_in, 2).decode()  # czytanie 2 bajtĂłw
try:
    result = os.read(fifo_in, int(r))
    print("Wynik: %s" % result.decode())
except ValueError as ve:
    print("Ojoj")
    print(ve)

os.unlink(C_FIFO)
