import os
import errno
import signal
import sys
import time


def populate(database):
    database.append({'id': 1, 'name': 'Jan Kowalski'})
    database.append({'id': 2, 'name': 'Adam Nowak'})
    database.append({'id': 3, 'name': 'Anna Wiśniewska'})
    database.append({'id': 4, 'name': 'Piotr Kowalczyk'})
    database.append({'id': 5, 'name': 'Krzysztof Lewandowski'})
    database.append({'id': 6, 'name': 'Barbara Dąbrowska'})
    database.append({'id': 7, 'name': 'Tomasz Zając'})
    return database


def search(database, id):
    for person in database:
        if person['id'] == id:
            return person['name']
    return "Nie ma"


def handler_kill(signum, frame):
    print('Zamykam program', signum)
    os.unlink(FIFO)
    sys.exit(0)


def handler_ignore(signum, frame):
    print('Ignoruję sygnał', signum)
    print()


signal.signal(signal.SIGUSR1, handler_kill)
signal.signal(signal.SIGTERM, handler_ignore)
signal.signal(signal.SIGHUP, handler_ignore)

FIFO = 'kolejka'


# baza danych
people = []
people = populate(people)

# utworzenie kolejki
try:
    os.mkfifo(FIFO)
except OSError as oe:
    if oe.errno != errno.EEXIST:
        raise

fifo_in = os.open(FIFO, os.O_RDONLY)
fifo_out1 = os.open(FIFO, os.O_WRONLY | os.O_NDELAY)

while True:
    r = os.read(fifo_in, 2)  # czytanie 2 bajtĂłw
    try:
        record = os.read(fifo_in, 2)
        client = os.read(fifo_in, int(r))
        print("Rekord: %s" % record.decode())
        print("Klient: %s" % client.decode())
        result = search(people, int(record))
        print("Wynik: %s" % result)
        print()
        fifo_out = os.open(client.decode(), os.O_WRONLY)
        if len(str(result)) < 10:
            len_res = "0" + str(len(str(result)))
        else:
            len_res = str(len(str(result)))
        os.write(fifo_out, (len_res + str(result)).encode())
    except ValueError as ve:
        print("Ojoj")
        print(ve)
    time.sleep(15)  # spowolnienie do testowania
