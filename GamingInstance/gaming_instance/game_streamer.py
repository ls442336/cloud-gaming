from threading import Thread
import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription
from gaming_instance.logger import logger
import logging
import json
from gaming_instance.exception import InvalidOffer
from gaming_instance.packet import Packet
import socket
import base64
import time
import win32com.client as comclt
from ctypes import *
user32 = windll.user32

wsh = comclt.Dispatch("WScript.Shell")

frame = None
lastId = -1
sended = 0


class WebRTCClient(Thread):
    def __init__(self, offer, host='127.0.0.1', port=6000, gameManager=None):
        Thread.__init__(self)

        self.logger = logging.getLogger("WebRTCClient")
        self.offer = offer
        self.is_answer_ready = False
        self.pc = None
        self.dataChannel = None
        self.pingChannel = None
        self.runner = None
        self.has_error = None
        self.lastId = -1
        self.send_enabled = False
        self.frame = None
        self.gameManager = gameManager
        self.hasGameBeenActivated = False

        self.host = host
        self.port = port
        self.lastPacketId = -1

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.s.bind((self.host, self.port))

    def extractPacketId(self, data):
        return int.from_bytes(data[-4:], 'big')

    def extractPacketFrame(self, data):
        return data[:-4]

    async def simulate_key_presses(self, data):
        lastTime = None
        for event in data['events']:
            if lastTime is not None:
                await asyncio.sleep((event['time'] - lastTime) / 1000.0)

            lastTime = event['time']

            if event['type'] == 'key_down':
                wsh.AppActivate(self.gameManager.target.pid)
                wsh.SendKeys(event['key'])
            # elif event['type'] == 'mouse_move':
            #     user32.SetCursorPos(
            #         int(event['x'] * 1280), int(event['y'] * 720))
            # elif event['type'] == 'mouse_down':
            #     user32.mouse_event(2, 0, 0, 0, 0)
            # elif event['type'] == 'mouse_up':
            #     user32.mouse_event(4, 0, 0, 0, 0)

    async def start_connection(self, payload):
        offer = None

        try:
            offer = RTCSessionDescription(
                sdp=payload["sdp"], type=payload["type"])
        except:
            raise InvalidOffer()

        self.pc = RTCPeerConnection()

        @self.pc.on("datachannel")
        def on_datachannel(channel):
            @channel.on("message")
            def on_message(message):
                if channel.label == 'data':
                    data = json.loads(message)

                    packet = Packet(id=self.lastPacketId,
                                    timestamp=data['timestamp'])

                    if self.send_enabled:
                        data, _ = self.s.recvfrom(65535)
                        packet.data = data

                    channel.send(packet.pack())

                    self.lastPacketId += 1
                elif channel.label == 'input':
                    data = json.loads(message)

                    if self.send_enabled:
                        loop = asyncio.get_event_loop()

                        asyncio.ensure_future(
                            self.simulate_key_presses(data))

                    channel.send('input_received')

            @self.pc.on("iceconnectionstatechange")
            async def on_iceconnectionstatechange():
                try:
                    self.logger.info("ICE connection state is %s",
                                     self.pc.iceConnectionState)

                    if self.pc.iceConnectionState == "failed":
                        await self.pc.close()
                except Exception as e:
                    self.logger.error(e)

        # handle offer
        try:
            await self.pc.setRemoteDescription(offer)
        except:
            raise InvalidOffer()

        # send answer
        answer = await self.pc.createAnswer()
        await self.pc.setLocalDescription(answer)

        return {"sdp": self.pc.localDescription.sdp,
                "type": self.pc.localDescription.type}

    def create_channel(self, offer):
        try:
            self.loop = asyncio.new_event_loop()

            self.answer = self.loop.run_until_complete(
                self.start_connection(offer))
            self.is_answer_ready = True
        except Exception as e:
            self.logger.error(e)
            raise Exception('Erro ao criar o canal')

    def run(self):
        self.create_channel(self.offer)

        self.loop.run_forever()

        self.logger.info('THREAD TERMINADA')

    def stop(self):
        try:
            self.s.close()
        except:
            pass

        if self.pc is not None:
            try:
                self.loop.run_until_complete(self.pc.close())
            except Exception as e:
                self.logger.error(e)

        self.pc = None
        self.channel = None

        try:
            self.loop.stop()
        except Exception as e:
            self.logger.warning(e)


class FrameReceiver(Thread):
    def __init__(self, host='127.0.0.1', port=6000):
        Thread.__init__(self)

        self.host = host
        self.port = port
        self.lastPacketId = -1

        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def extractPacketId(self, data):
        return int.from_bytes(data[-4:], 'big')

    def extractPacketFrame(self, data):
        return data[:-4]

    def run(self):
        self.s.bind((self.host, self.port))

        while True:
            global frame

            data, address = self.s.recvfrom(65535)

            try:
                packetId = self.extractPacketId(data)

                if packetId > self.lastPacketId:
                    data = self.extractPacketFrame(data)
                    self.lastPacketId = packetId

                    frame = {
                        "id": packetId,
                        "data": 'data:image/jpeg;base64,' + base64.b64encode(data).decode('utf-8')
                    }
                else:
                    frame = None
            except:
                pass

    def clear(self):
        self.lastPacketId = -1


class GameStreamer:
    sender = None
    receiver = None

    lastId = -1

    sended = 0
    last = time.time()

    def init(self):
        # self.receiver = FrameReceiver()
        # self.receiver.start()
        pass

    def create_channel(self, offer, gameManager):
        self.sender = WebRTCClient(offer, gameManager=gameManager)
        self.sender.start()

    def stop(self):
        if self.sender is not None:
            self.sender.stop()

        self.sender = None

    def stream(self):
        time.sleep(0.3)
