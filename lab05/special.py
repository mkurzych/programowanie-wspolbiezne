import sysv_ipc


input_queue = sysv_ipc.MessageQueue(1234)
input_queue.send("stop".encode(), type=1)

