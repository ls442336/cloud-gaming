from gaming_instance.state import State
from gaming_instance.game_downloader import State as GameDownloaderState
import time
import json
from threading import Thread
import os
import zipfile


def handle_start_connection(self):
    self.logger.info('Conectando-se ao Gerenciador de Partidas')

    self.connManager.createConnection()

    if self.connManager.getConnection() is None:
        self.logger.error('Erro ao se conectar ao Gerenciador de Partidas')
        self.changeState(State.RETRY_CONNECTION)
    else:
        self.changeState(State.REGISTER)


def handle_retry_connection(self):
    self.logger.info(
        'Iniciando nova tentativa de conexão ao Gerenciador de Partidas')
    time.sleep(1)
    self.changeState(State.START_CONNECTION)


def handle_register(self):
    self.logger.info('Tentando se registrar')

    conn = self.connManager.getConnection()

    if conn is None:
        self.changeState(State.CONNECTION_LOST)
        return

    conn.send({
        "route": 'register_instance'
    })

    self.changeState(State.WAITING_REGISTRATION)


def handle_connection_lost(self):
    self.logger.error('Conexão perdida com o Gerenciador de Partidas')

    # limpar estados
    self.logger.info('Limpando estados')
    self.clearStates()

    self.changeState(State.RETRY_CONNECTION)


def handle_end_session(self):
    self.context.session = None
    self.streamer.stop()
    self.changeState(State.IDLE)


def handle_waiting_answer(self):
    if self.streamer.sender.is_answer_ready:
        answer = self.streamer.sender.answer
        conn = self.connManager.getConnection()

        conn.send({
            'route': 'gaming_instance/answer',
            'answer': answer,
            'session_id': self.context.session.id
        })

        self.changeState(State.WAITING_ANSWER_CONFIRMATION)
    elif self.streamer.sender.has_error:
        self.logger.error('Oferta inválida: ')

        conn = self.connManager.getConnection()

        conn.send({
            "route": "gaming_instance/invalid_offer",
            'instance': self.context.instance
        })

        self.changeState(State.WAITING_SESSION_TO_END)

        return


def handle_streaming(self):
    pass


def handle_download_game(self):
    # Verifica se o download terminou
    downloadInstance = self.gameDownloader.getDownload()
    conn = self.connManager.getConnection()

    if downloadInstance is None or downloadInstance.status == GameDownloaderState.ERROR:
        self.logger.error('Erro no download')
        conn.send({
            'route': 'gaming_instance/download_error',
            'instance': self.context.instance
        })
        self.changeState(State.WAITING_SESSION_TO_END)
    elif downloadInstance.status == GameDownloaderState.DONE:
        try:
            games_folder = os.environ.get("GAMES_FOLDER")
            game_path = os.path.join(games_folder, 'game.zip')

            with zipfile.ZipFile(game_path, 'r') as zip_ref:
                zip_ref.extractall(games_folder)

            conn.send({
                'route': 'gaming_instance/download_done',
                'instance': self.context.instance
            })

            self.changeState(State.DOWNLOAD_DONE)
        except Exception as e:
            self.logger.error(e)

            self.logger.error('Erro no download')
            conn.send({
                'route': 'gaming_instance/download_error',
                'instance': self.context.instance
            })
            self.changeState(State.WAITING_SESSION_TO_END)


def handle_waiting_download_end_session(self):
    downloadInstance = self.gameDownloader.getDownload()

    if downloadInstance is None or downloadInstance.status == GameDownloaderState.ERROR or downloadInstance.status == GameDownloaderState.DONE:
        self.clearStates()
        self.changeState(State.IDLE)

        conn = self.connManager.getConnection()

        conn.send({
            "route": "gaming_instance/ready",
            "instance": self.context.instance
        })
