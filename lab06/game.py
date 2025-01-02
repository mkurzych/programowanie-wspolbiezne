import sysv_ipc
import time
import os
import argparse

SHM_KEY1 = 1234
SHM_KEY2 = 5678
SEM_KEY1 = 1111
SEM_KEY2 = 2222


def cleanup(SHM_KEY1, SHM_KEY2, SEM_KEY1, SEM_KEY2):
    try:
        shm1 = sysv_ipc.SharedMemory(SHM_KEY1)
        shm1.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        shm2 = sysv_ipc.SharedMemory(SHM_KEY2)
        shm2.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        sem1 = sysv_ipc.Semaphore(SEM_KEY1)
        sem1.remove()
    except sysv_ipc.ExistentialError:
        pass

    try:
        sem2 = sysv_ipc.Semaphore(SEM_KEY2)
        sem2.remove()
    except sysv_ipc.ExistentialError:
        pass


try:
    shm1 = sysv_ipc.SharedMemory(SHM_KEY1, sysv_ipc.IPC_CREX, size=1024)
    shm2 = sysv_ipc.SharedMemory(SHM_KEY2, sysv_ipc.IPC_CREX, size=1024)
    player = 1
except sysv_ipc.ExistentialError:
    shm1 = sysv_ipc.SharedMemory(SHM_KEY1)
    shm2 = sysv_ipc.SharedMemory(SHM_KEY2)
    player = 2

try:
    sem1 = sysv_ipc.Semaphore(SEM_KEY1, sysv_ipc.IPC_CREX, initial_value=0)
    sem2 = sysv_ipc.Semaphore(SEM_KEY2, sysv_ipc.IPC_CREX, initial_value=0)
except sysv_ipc.ExistentialError:
    sem1 = sysv_ipc.Semaphore(SEM_KEY1)
    sem2 = sysv_ipc.Semaphore(SEM_KEY2)


def write_to_shm(shm, message):
    shm.write(message.encode())


def read_from_shm(shm):
    return shm.read().decode().strip('\x00')


def main():
    score1 = 0
    score2 = 0

    for round in range(3):
        if player == 1:
            position = input("Gracz 1: Wybierz pozycję wygrywającej karty (1, 2, 3): ")
            write_to_shm(shm1, position)
            sem1.release()

            sem2.acquire()
            guess = read_from_shm(shm2)
            print(f"Gracz 2 wybrał pozycję: {guess}")

            if position == guess:
                print("Gracz 2 wygrał tę turę!")
                score2 += 1
            else:
                print("Gracz 1 wygrał tę turę!")
                score1 += 1

        else:
            sem1.acquire()
            position = read_from_shm(shm1)
            guess = input("Gracz 2: Wybierz pozycję (1, 2, 3): ")
            write_to_shm(shm2, guess)
            sem2.release()

            print(f"Gracz 1 wybrał pozycję: {position}")

            if position == guess:
                print("Gracz 2 wygrał tę turę!")
                score2 += 1
            else:
                print("Gracz 1 wygrał tę turę!")
                score1 += 1

        print(f"Wynik po {round + 1} turach: Gracz 1 - {score1}, Gracz 2 - {score2}")

    if player == 1:
        cleanup(SHM_KEY1, SHM_KEY2, SEM_KEY1, SEM_KEY2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Three-card game with shared memory and semaphores.")
    parser.add_argument('-r', '--remove', action='store_true', help="Remove shared memory and semaphores")
    args = parser.parse_args()

    if args.remove:
        cleanup(SHM_KEY1, SHM_KEY2, SEM_KEY1, SEM_KEY2)
    else:
        main()
