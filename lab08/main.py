import threading
from time import sleep


def sum_part(lst, start, end, result, index, lock):
    sleep(index * 0.2)
    print(f"Sumowanie części {index + 1}...")
    partial_sum = sum(lst[start:end])
    with lock:
        result[0] = result[0] + partial_sum


def sum_list_multiple_threads(lst, num_threads):
    n = len(lst)
    result = [0]
    threads = []
    lock = threading.Lock()

    chunk_size = n // num_threads
    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else n
        thread = threading.Thread(target=sum_part, args=(lst, start, end, result, i, lock))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result[0]


large_list = list(range(1, 1000001))
num_threads = int(input("Podaj ilość wątków: "))
total_sum = sum_list_multiple_threads(large_list, num_threads)

print(f"Suma całkowita wątkowa: {total_sum}")
print(f"Suma całkowita wbudowana: {sum(large_list)}")
