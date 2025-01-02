import time
import math
from multiprocessing import Pool


def is_prime_small(k):
    for i in range(2, k - 1):
        if i * i > k:
            return True
        if k % i == 0:
            return False
    return True


def is_prime_with_small_primes(k, small_primes):
    for p in small_primes:
        if k % p == 0:
            return False
        if p * p > k:
            return True
    return True


def get_small_primes(upper_bound):
    small_primes = []
    s = math.ceil(math.sqrt(upper_bound))
    for i in range(2, s + 1):
        if is_prime_small(i):
            small_primes.append(i)
    return small_primes


def find_twin_primes_sequential(start, end):
    small_primes = get_small_primes(end)
    twin_primes = []

    for i in range(start, end - 1):
        if is_prime_with_small_primes(i, small_primes) and is_prime_with_small_primes(i + 2, small_primes):
            twin_primes.append((i, i + 2))

    return twin_primes


def check_range_for_twins(args):
    start, end, small_primes = args
    local_twins = []

    for i in range(start, end):
        if is_prime_with_small_primes(i, small_primes) and is_prime_with_small_primes(i + 2, small_primes):
            local_twins.append((i, i + 2))

    return local_twins


def find_twin_primes_parallel(start, end, num_processes):

    small_primes = get_small_primes(end)

    chunk_size = (end - start) // num_processes
    ranges = []
    for i in range(num_processes):
        chunk_start = start + i * chunk_size
        chunk_end = chunk_start + chunk_size if i < num_processes - 1 else end
        ranges.append((chunk_start, chunk_end, small_primes))

    with Pool(processes=num_processes) as pool:
        results = pool.map(check_range_for_twins, ranges)

    #  map(func, iterable[, chunksize])
    #     A parallel equivalent of the map() built-in function.
    #     It blocks until the result is ready.
    #     https://docs.python.org/3.11/library/functions.html#map

    twin_primes = []
    for chunk in results:
        for pair in chunk:
            twin_primes.append(pair)

    return twin_primes


def compare_implementations(start, end, num_processes_list):
    print(f"Finding twin primes in range [{start}, {end}]")

    # Sequential implementation
    print("\nSequential:")
    start_time = time.time()
    sequential_results = find_twin_primes_sequential(start, end)
    sequential_time = time.time() - start_time
    print(f"Time: {sequential_time:.2f} seconds")
    print(f"Pair primes: {len(sequential_results)}")

    # Parallel implementation with different numbers of processes
    print("\nParallel:")
    for num_processes in num_processes_list:
        print(f"\n{num_processes} processes:")
        start_time = time.time()
        parallel_results = find_twin_primes_parallel(start, end, num_processes)
        parallel_time = time.time() - start_time
        print(f"Time: {parallel_time:.2f} seconds")
        print(f"Speedup: {sequential_time / parallel_time:.2f}x")
        print(f"Pair primes: {len(parallel_results)}")


if __name__ == '__main__':
    l = 1000000
    r = 2000000
    num_processes_to_test = [2, 4, 6, 8]

    compare_implementations(l, r, num_processes_to_test)
