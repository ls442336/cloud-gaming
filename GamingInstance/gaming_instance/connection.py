from gaming_instance.logger import logger
from gaming_instance.singleton import SingletonMeta
from websocket import create_connection
from threading import Thread
import logging
import time
import os
import json


class Connection(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)

        self.host = host
        self.port = port
        self.isRunning = False
        self.isRetrying = False
        self.messages = []

        self.logger = logging.getLogger('WebSocketsClient')

    def init(self):
        try:
            self.ws = create_connection(self.getEndpoint())
            self.isRunning = True

            self.logger.info('Conexão de websockets bem sucedida')

            return True
        except:
            self.logger.error(
                'Falha ao estabelecer comunicação com Gerenciador de Partidas')

        return False

    def getEndpoint(self):
        return "ws://" + str(self.host) + ":" + str(self.port)

    def send(self, payload):
        data = None

        try:
            data = json.dumps(payload)
        except:
            self.logger.error('Payload inválido')
            return False

        try:
            self.ws.send(data)
        except:
            self.logger.error(
                'Erro ao enviar dados para o Gerenciador de Partidas')
            self.logger.info('Encerrando conexão')
            self.close()
            return False

        return True

    def close(self):
        self.isRunning = False

        try:
            self.ws.close()
        except:
            pass

    def clear(self):
        self.messages = []

    def run(self):
        while self.isRunning:
            try:
                data = self.ws.recv()
                self.messages.append(data)

                self.logger.info(
                    "Mensagem recebida do Coordenador de Partidas")
            except:
                self.close()


class ConnectionManager:
    conn = None

    def getConnection(self):
        if self.conn is not None and not self.conn.isRunning:
            self.conn = None

        return self.conn

    def createConnection(self):
        if self.conn == None:
            self.conn = Connection(os.environ.get(
                "HOST"), os.environ.get("PORT"))

            if self.conn.init():
                self.conn.start()
                return True
            else:
                self.conn = None

        return False

    def clear(self):
        self.conn.close()
        self.conn = None
