import threading
from threading import Barrier, Lock
import math


def is_prime(k):
    for i in range(2, k-1):
        if i * i > k:
            return True
        if k % i == 0:
            return False
    return True


def find_primes_in_range(start, end, primes, lock, barrier):
    local_primes = []
    for num in range(start, end + 1):
        if is_prime(num):
            local_primes.append(num)

    with lock:
        for prime in local_primes:
            primes.append(prime)

    barrier.wait()


def find_primes_parallel(start, end, num_threads):
    primes = []
    lock = Lock()
    barrier = Barrier(num_threads + 1)
    threads = []

    range_size = (end - start + 1) // num_threads

    for i in range(num_threads):
        thread_start = start + i * range_size
        thread_end = thread_start + range_size - 1
        if i == num_threads - 1:
            thread_end = end

        thread = threading.Thread(
            target=find_primes_in_range,
            args=(thread_start, thread_end, primes, lock, barrier)
        )
        threads.append(thread)
        thread.start()

    barrier.wait()

    primes.sort()
    return primes


def main():
    start = int(input("Podaj początek przedziału: "))
    end = int(input("Podaj koniec przedziału: "))
    num_threads = int(input("Podaj liczbę wątków: "))

    start_true = start
    if start_true < 2:
        start_true = 2

    primes = find_primes_parallel(start_true, end, num_threads)

    pierwsze = []

    for i in range(start_true, end + 1):
        if is_prime(i):
            pierwsze.append(i)

    print(f"\nSekwencyjnie znalezione liczby pierwsze w przedziale [{start}, {end}]:")
    print(pierwsze)
    print(f"Liczba znalezionych liczb pierwszych: {len(pierwsze)}")

    print(f"\nWielowątkowo znalezione liczby pierwsze w przedziale [{start}, {end}]:")
    print(primes)
    print(f"Liczba znalezionych liczb pierwszych: {len(primes)}")
    print(f"Liczba użytych wątków: {num_threads}")


if __name__ == "__main__":
    main()
