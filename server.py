import asyncio
import os
import signal
import subprocess
import GPUtil
import psutil
from screeninfo import get_monitors
import logging


logfile = "server.log"
f = open(logfile, 'w')
f.close()

logging.basicConfig(
    level=logging.DEBUG,
    filename = logfile,
    # format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    format = "%(asctime)s - %(levelname)s - %(funcName)s(): %(message)s",
    datefmt='%H:%M:%S',
    )

def format_bytes(size, label):
    if label == "B":
        size = size
    elif label == "KB":
        size = size / 1024
    elif label == "MB":
        size = size / (1024 * 1024)
    elif label == "GB":
        size = size / (1024 * 1024 * 1024)
    elif label == "TB":
        size = size / (1024 * 1024 * 1024 * 1024)
    else :
        size = 0
    return size

def getGPUname():
    return GPUtil.getGPUs()[0].name

def signalFunc(signum,frame):
    print("\n\nServer paused...")
    data = input("Type command (you can use help):")
    if data == "help":
        print("close - закрывает сервак\nlogs-открыть логи(GUI)")
        print("Sever unpaused...\n\n")
        return
    if data == "close":
        os.kill(os.getpid(), signal.SIGKILL)
        return
    if data == "logs":
        subprocess.Popen(["python", "server__logs.py"], shell=True)
        print("Sever unpaused...\n\n")
        return


async def handle_connection(reader, writer):
    addr = writer.get_extra_info("peername")
    print("Client", addr, "connected")
    logging.info("Client " + str(addr) + " connected")
    serverid = 1
    while True:
        try:
            data = await reader.read(1024)  # New
        except ConnectionError:
            print(f"Client {addr} closed connection ")
            logging.info(f"Client {addr} closed connection ")
            break
        print(f"Received '{data}' from: {addr}")
        logging.info(f"Received '{data}' from: {addr}")
        if not data:
            break
        senddata = str.encode("Unknown command")
        if data == b"close":
            logging.info(f"Client {addr} closed server")
            break
        if data == b'switch':
            if serverid == 1:
                serverid = 2
                senddata = str.encode("Switched to server 2")
            else:
                serverid = 1
                senddata = str.encode("Switched to server 1")

        elif serverid == 1:
            if data == b"GPU":
                try:
                    name = getGPUname()
                    senddata = str.encode("Название видеопроцессора: " + name)
                except Exception:
                    senddata = str.encode("Не получилось получить имя видеопроцессора")
            if data == b"screen":
                try:
                    name =  str(get_monitors()[0].width) +"x" +  str(get_monitors()[0].height)
                    senddata = str.encode("Размер экрана: " + name)
                except Exception:
                    senddata = str.encode("Не получилось получить размера экрана")
        elif serverid == 2:
            if data == b"swap":
                try:
                    senddata = str.encode("Свободных байтов файла подкачки " + str(psutil.swap_memory().free) + " из " + str(psutil.swap_memory().total))
                except Exception:
                    senddata = str.encode("Не получилось получить данные о файле подкачки")
            if str(data).startswith("b'memory"):
                data = str(data)
                label = data[data.find(' ')+1:data.__len__() - 1]
                try:
                    used = round(format_bytes(psutil.virtual_memory().used, label),2)
                    total = round(format_bytes(psutil.virtual_memory().total, label),2)
                    if used != 0:
                        senddata = str.encode(f"Физическая память: Используется {used}{label} из {total}{label}")
                    else:
                        senddata = str.encode("Кажется вы ошиблись. Использование команды memory B/MB/KB/GB/TB. Не забудьте указать единицу измерения")
                except Exception:

                    senddata = str.encode("Не получилось получить физическую память")

        print(f"Send: '{senddata}' to: {addr}")
        logging.info(f"Send: '{senddata}' to: {addr}")
        try:
            writer.write(senddata)  # New
            await writer.drain()
        except ConnectionError:
            print(f"Client {addr} closed connection")
            logging.info(f"Client {addr} closed connection ")
            break
    writer.close()
    print("Client", addr, "disconnected")
    logging.info(f"Client {addr} disconnected")

    
async def main(host, port):
    server = await asyncio.start_server(handle_connection, host, port)
    logging.info(f"Start server...")
    print(f"Start server...")
    async with server:
        await server.serve_forever()

HOST = ""
PORT = 50007

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signalFunc)
    asyncio.run(main(HOST, PORT))

