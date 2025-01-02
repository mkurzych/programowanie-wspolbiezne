import sysv_ipc
import time


input_queue = sysv_ipc.MessageQueue(1234, sysv_ipc.IPC_CREAT)
output_queue = sysv_ipc.MessageQueue(5678, sysv_ipc.IPC_CREAT)

dictionary = {
    "hello": "cześć",
    "world": "świat",
    "cat": "kot",
    "dog": "pies"
}

while True:
    message, message_type = input_queue.receive()
    if message.decode() == "stop":
        break

    pid, word = message.decode().split(',')
    response = dictionary.get(word, "Nie znam takiego słowa")

    time.sleep(2)
    output_queue.send(response.encode(), type=int(pid))

input_queue.remove()
output_queue.remove()


