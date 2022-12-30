# # GPU information
# import GPUtil
# from tabulate import tabulate
# print("="*40, "GPU Details", "="*40)
# gpus = GPUtil.getGPUs()
# list_gpus = []
# for gpu in gpus:
#     # get the GPU id
#     gpu_id = gpu.id
#     # name of GPU
#     gpu_name = gpu.name
#     # get % percentage of GPU usage of that GPU
#     gpu_load = f"{gpu.load*100}%"
#     # get free memory in MB format
#     gpu_free_memory = f"{gpu.memoryFree}MB"
#     # get used memory
#     gpu_used_memory = f"{gpu.memoryUsed}MB"
#     # get total memory
#     gpu_total_memory = f"{gpu.memoryTotal}MB"
#     # get GPU temperature in Celsius
#     gpu_temperature = f"{gpu.temperature} °C"
#     gpu_uuid = gpu.uuid
#     list_gpus.append((
#         gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
#         gpu_total_memory, gpu_temperature, gpu_uuid
#     ))
#
# print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
#                                    "temperature", "uuid")))


# import subprocess
# output = subprocess.getoutput("dir")
# print(output)


# import time
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
#
# class MyHandler(FileSystemEventHandler):
#     def on_any_event(self, event):
#         print(event.event_type, event.src_path)
#
#     def on_created(self, event):
#         print("on_created", event.src_path)
#
#     def on_deleted(self, event):
#         print("on_deleted", event.src_path)
#
#     def on_modified(self, event):
#         print("on_modified", event.src_path)
#
#     def on_moved(self, event):
#         print("on_moved", event.src_path)
#
#
# event_handler = MyHandler()
# observer = Observer()
# observer.schedule(event_handler, path='.', recursive=False)
# observer.start()
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()


# import os
# os.spawnl(os.P_DETACH, 'python server__class.py')

# import subprocess
# subprocess.Popen(["python", "server__class.py"], shell=True)
# # os.system("python server__class.py &")
# print("faf")


# import os
# import time
# import signal
#
# def func(signum, frame):
#     print (f"You raised a SigInt! Signal handler called with signal {signum}")
#
# signal.signal(signal.SIGINT, func)
# while True:
#     print(f"Running...{os.getpid()}")
#     time.sleep(2)

# a = "b'memory GB'"
# print()


import asyncio
import tkinter as tk

class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.transport.write(data)

    def connection_lost(self, exc):
        pass

class EchoClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print(data.decode())

    def connection_lost(self, exc):
        pass

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.server = None
        self.start_button = tk.Button(master, text="Start Server", command=self.start_server)
        self.start_button.pack()
        self.stop_button = tk.Button(master, text="Stop Server", command=self.stop_server)
        self.stop_button.pack()

    def start_server(self):
        loop = asyncio.get_event_loop()
        coro = loop.create_server(EchoServerProtocol, 'localhost', 8000)
        self.server = loop.run_until_complete(coro)
        print('Serving on {}'.format(self.server.sockets[0].getsockname()))

    def stop_server(self):
        self.server.close()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.server.wait_closed())

class ClientGUI:
    def __init__(self, master):
        self.master = master
        self.client = None
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack()
        self.message_entry = tk.Entry(master)
        self.message_entry.pack()

    def send_message(self):
        message = self.message_entry.get()
        self.client.transport.write(message.encode())

root = tk.Tk()
root.title("Asyncio GUI")
server_frame = tk.Frame(root)
server_frame.pack()
client_frame = tk.Frame(root)
client_frame.pack()
server_gui = ServerGUI(server_frame)
client_gui = ClientGUI(client_frame)
root.mainloop()