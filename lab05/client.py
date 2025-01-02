import sysv_ipc
import os


input_queue = sysv_ipc.MessageQueue(1234)
output_queue = sysv_ipc.MessageQueue(5678)
pid = os.getpid()

word = input("Enter a word: ")


for _ in range(5):
    input_queue.send(f"{pid},{word}".encode(), type=1)
    response, response_type = output_queue.receive(type=int(pid))
    print(f"Response for '{word}': {response.decode()}")

