# Попытка написать все классами, зачем я не понял, но в принципе у меня ничего не получилось...

import asyncio
import tkinter as tk
import GPUtil
import logging

logfile = "server.log"
# f = open(logfile, 'w')
# f.close()

logging.basicConfig(
    level=logging.DEBUG,
    filename = logfile,
    # format = "%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    format = "%(asctime)s - %(levelname)s - %(funcName)s(): %(message)s",
    datefmt='%H:%M:%S',
    )



class Server():
    active = False

    def __init__(self, host="", port=48882, serverId=1, ):

        self.host = host
        self.port = port
        self.serverHandler = self.first if serverId == 1 else self.second
        # self.logfunc = logfunc

    async def first(self, reader, writer):
        addr = writer.get_extra_info("peername")
        print("Connected by", addr)
        logging.info("Connected by" + str(addr))
        # self.logfield.config(state="normal")
        # self.logfield.insert(1.0, "Я сосал меня ебали")
        # self.logfield.config(state="disabled")
        # self.logfunc("privet")
        while self.active:
            try:
                data = await reader.read(1024)  # New
            except ConnectionError:
                print(f"Client suddenly closed while receiving from {addr}")
                break
            print(f"Received {data} from: {addr}")
            if not data:
                await self.stop(writer)

            if data == b"close":
                await self.stop(writer)
            senddata = data

            try:
                writer.write(senddata)  # New
                await writer.drain()
                print(f"Send: {senddata} to: {addr}")
            except ConnectionError:
                logging.info("Some error while sending")
                print(f"Some error while sending ;c ")
                break

        writer.close()
        print("Disconnected by", addr)
        logging.info("Disconnected by" + str(addr))

    def s(self):

        asyncio.run(self.start())

    async def start(self):
        self.active = True
        server = await asyncio.start_server(self.serverHandler, self.host, self.port)
        print("Start server... ")
        logging.info("Start server... ")
        async with server:
            await server.serve_forever()

    async def stop(self, writer):
        try:
            writer.write(b"server closed")  # New
            logging.info("Server closed")
            await writer.drain()
        except ConnectionError:
            print(f"Client suddenly closed, cannot send")
            logging.info("Client suddenly closed, cannot send")
        self.active = False


if __name__ == '__main__':
    server = Server()
    asyncio.run(server.start())
