class Session:
    id = None
    game = None

    def __init__(self, id=None, game=None):
        self.id = id
        self.game = game

    @staticmethod
    def from_dict(session):
        obj = Session()

        obj.id = session['id']
        obj.game = Game.from_dict(session['game'])

        return obj


class Game:
    id = None
    path = None
    bucket_id = None

    def __init__(self, id=None, path=None, bucket_id=None):
        self.id = id
        self.path = path
        self.bucket_id = bucket_id

    @staticmethod
    def from_dict(game):
        obj = Game()

        obj.id = game['id']
        obj.path = game['path']
        obj.bucket_id = game['bucket_id']

        return obj
