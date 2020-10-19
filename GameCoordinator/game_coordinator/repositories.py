from game_coordinator.singleton import SingletonMeta
from game_coordinator.repository import Repository


class ConnectionRepository(Repository, metaclass=SingletonMeta):
    def __init__(self):
        Repository.__init__(self)
