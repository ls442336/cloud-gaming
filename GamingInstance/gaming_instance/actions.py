from gaming_instance.state import State
from gaming_instance.models import Session
import os


def start_session(self, data):
    self.logger.info('Pedido de sessão recebido')

    if self.context.state == State.IDLE:
        session = None

        try:
            session = Session.from_dict(data['session'])
        except:
            self.logger.error('Estrutura de sessão inválida')
            return

        self.context.session = session

        conn = self.connManager.getConnection()
        result = conn.send({
            'route': 'gaming_instance/confirm_session',
            'instance': self.context.instance,
            'session_id': session.id
        })

        if not result:
            return

        self.changeState(State.WAITING_OFFER)


def end_session(self, data):
    if self.context.state == State.DOWNLOADING_GAME:
        self.changeState(State.WAITING_DOWNLOAD_END_SESSION)
        return

    self.clearStates()
    self.changeState(State.IDLE)

    conn = self.connManager.getConnection()

    conn.send({
        "route": "gaming_instance/ready",
        "instance": self.context.instance
    })


def get_answer(self, data):
    offer = data['offer']

    self.streamer.create_channel(offer, self.gameManager)

    self.changeState(State.WAITING_ANSWER)


def download_game(self, data):
    try:
        bucket_name = os.environ.get("BUCKET_NAME")
        games_folder = os.environ.get("GAMES_FOLDER")

        object_id = self.context.session.game.bucket_id
        path = self.context.session.game.path

        game_path = os.path.join(games_folder, 'game.zip')

        self.gameDownloader.download(bucket_name, object_id, game_path)

        self.changeState(State.DOWNLOADING_GAME)
    except Exception as e:
        conn = self.connManager.getConnection()
        conn.send({
            'route': 'gaming_instance/download_error',
            'instance': self.context.instance
        })

        self.changeState(State.WAITING_SESSION_TO_END)
        self.logger.error(e)


def open_game(self, data):
    games_folder = os.environ.get("GAMES_FOLDER")
    path = self.context.session.game.path
    game_path = os.path.join(games_folder, path)

    self.gameManager.open(game_path)  # TODO: chance de erro

    conn = self.connManager.getConnection()

    conn.send({
        'route': 'gaming_instance/game_openned',
        'instance': self.context.instance
    })

    self.streamer.sender.send_enabled = True

    self.changeState(State.WAITING_TO_STREAM)


def stream(self, data):
    self.changeState(State.STREAMING)
