import os
import tkinter as tk
import asyncio
import server__class
import subprocess
import threading
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

updateLog = None
updateStatus = None

class MyHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # print(event.event_type, event.src_path)
        if event.event_type == "modified" and event.src_path == ".\server.log":
            try:
                updateLog()
            except Exception:
                return

    # def on_created(self, event):
    #     print("on_created", event.src_path)
    #
    # def on_deleted(self, event):
    #     print("on_deleted", event.src_path)
    #
    # def on_modified(self, event):
    #     print("on_modified", event.src_path)
    #
    # def on_moved(self, event):
    #     print("on_moved", event.src_path)


class ServerWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.top = tk.Frame(self)
        self.left = tk.Frame(self)
        self.right = tk.Frame(self)

        self.textLog = tk.Text(self.left, state='disabled', height=12)
        self.textStatus = tk.Text(self.right, state='disabled', height=10, width=12)

        self.buttonStart = tk.Button(self.right, text="Обновить логи", width=12, command=self.startButtonHandler)

        self.label = tk.Label(self.top, text="Логи сервака", font='Helvetica 18 bold')

        self.top.pack(side=tk.TOP, fill=tk.Y)
        self.left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.right.pack(side=tk.RIGHT, fill=tk.Y)

        self.textLog.pack(side=tk.LEFT)
        self.textStatus.pack(side=tk.TOP)
        self.buttonStart.pack(side=tk.TOP)

        self.label.pack(side=tk.TOP)

        self.updatelog()
        self.logIndex = 1.0

    def startButtonHandler(self):
        self.updatelog()


    # def addlogevent(self, data):
    #     self.textLog.config(state="normal")
    #     self.textLog.insert(self.logIndex, data)
    #     self.textLog.config(state="disabled")
    #     self.logIndex = self.logIndex + 1.0

    def updatelog(self):
        i = 1.0
        self.textLog.config(state="normal")
        self.textLog.delete("1.0", tk.END)
        with open("server.log") as file:
            while (line := file.readline().rstrip()):
                # self.textLog.delete("1.0", tk.END)
                print("line", line)
                # self.textLog.insert(i, "sss")
                self.textLog.insert("end", "\n" + str(line))
                i = i + 1.0

        self.textLog.config(state="disabled")

    # def clearlog(self):


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=False)
    observer.start()


    root = tk.Tk()
    # root.geometry("350x250")
    root.title("Главное окно")
    test = ServerWindow(root)
    updateLog = test.updatelog
    test.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

    observer.join()
