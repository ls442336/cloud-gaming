from gaming_instance.logger import logger
from gaming_instance.connection import ConnectionManager
from gaming_instance.handlers import *
from gaming_instance.state import State
from gaming_instance.actions import *
from gaming_instance.game_streamer import GameStreamer
from gaming_instance.game_manager import GameManager
from gaming_instance.game_downloader import GameDownloader
import logging
import os
import time
import json
import shutil
import psutil


class ApplicationContext:
    instance = None
    state = State.START_CONNECTION
    session = None


class Application:
    def __init__(self):
        self.logger = logging.getLogger('Application')

        self.handlers = {}
        self.actions = {}
        self.status = {}
        self.context = ApplicationContext()
        self.connManager = ConnectionManager()
        self.streamer = GameStreamer()
        self.gameManager = GameManager()
        self.gameDownloader = GameDownloader()

    def init(self):
        self.logger.info('Inicializando GameInstance')

        # Initialize context
        self.context.instance = os.environ.get("INSTANCE_ID")

        self.streamer.init()

        # Setup handlers
        self.handlers[State.START_CONNECTION] = handle_start_connection
        self.handlers[State.RETRY_CONNECTION] = handle_retry_connection
        self.handlers[State.REGISTER] = handle_register
        self.handlers[State.CONNECTION_LOST] = handle_connection_lost
        self.handlers[State.END_SESSION] = handle_end_session
        self.handlers[State.STREAMING] = handle_streaming
        self.handlers[State.DOWNLOADING_GAME] = handle_download_game
        self.handlers[State.WAITING_ANSWER] = handle_waiting_answer
        self.handlers[State.WAITING_DOWNLOAD_END_SESSION] = handle_waiting_download_end_session

        # Setup actions
        self.actions['start_session'] = start_session
        self.actions['get_answer'] = get_answer
        self.actions['download_game'] = download_game
        self.actions['open_game'] = open_game
        self.actions['stream'] = stream
        self.actions['end_session'] = end_session

    # Main methods
    def clearStates(self):
        self.context.session = None

        try:
            conn = self.connManager.getConnection()
            conn.clear()
        except:
            pass

        if self.gameDownloader.getDownload() is not None:
            self.gameDownloader.clear()

        try:
            self.gameManager.close()
            while self.gameManager.getStatus() == psutil.STATUS_RUNNING:
                pass

        except Exception as e:
            self.logger.warning('Erro ao fechar o jogo')
            self.logger.warning(e)

        try:
            self.streamer.stop()
        except Exception as e:
            self.logger.warning(e)

        # Deletar jogo
        games_folder = os.environ.get("GAMES_FOLDER")

        try:
            shutil.rmtree(games_folder)
        except Exception as e:
            self.logger.warning(e)

        # Criar diretório do jogo
        try:
            os.makedirs(games_folder, exist_ok=True)
        except Exception as e:
            self.logger.warning(e)

        time.sleep(5)

    def check_conn_status(self):
        states = [State.NONE, State.START_CONNECTION, State.RETRY_CONNECTION]

        conn = self.connManager.getConnection()

        if conn is not None:
            return True

        if self.context.state not in states:
            self.changeState(State.CONNECTION_LOST)

        return False

    def get_next_message(self):
        conn = self.connManager.getConnection()

        if conn is None:
            self.changeState(State.CONNECTION_LOST)
            return

        if len(conn.messages) > 0:
            msg = conn.messages.pop(0)

            return msg

        return None

    def handle_msg(self, msg):
        data = None

        try:
            data = json.loads(msg)
        except:
            pass

        if data is None:
            self.logger.warning(
                'Requisição inválida do Gerenciador de Partidas')
            return

        if 'type' in data:
            if data['type'] == 'action' and 'action' in data:
                self.handle_action(data)
            elif data['type'] == 'status' and 'status' in data:
                self.handle_status(data)
            else:
                self.logger.warning(
                    'Requisição inválida (operação) do Gerenciador de Partidas')
                return
        else:
            self.logger.warning(
                'Requisição inválida (estrutura) do Gerenciador de Partidas')
            return

    def handle_action(self, data):
        if data['action'] in self.actions:
            self.actions[data['action']](self, data)

    def handle_status(self, data):
        if data['status'] == 'register_success':
            if self.context.state == State.WAITING_REGISTRATION:
                self.logger.info(
                    'Registrado com sucesso, id = {}'.format(data['instance']))
                self.context.instance = data['instance']

                conn = self.connManager.getConnection()

                conn.send({
                    "route": "gaming_instance/ready",
                    "instance": self.context.instance
                })

                self.changeState(State.IDLE)

    def handle_state(self, state):
        if state in self.handlers:
            self.handlers[state](self)

    def changeState(self, state):
        self.logger.info(
            "Mudança de estado {} -> {}".format(self.context.state, state))
        self.context.state = state

    def mainloop(self):
        while True:
            status = self.check_conn_status()

            if status:
                msg = self.get_next_message()
                if msg is not None:
                    self.handle_msg(msg)

            self.handle_state(self.context.state)

            time.sleep(0.016)
