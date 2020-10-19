from game_coordinator.singleton import SingletonMeta
from pymongo import MongoClient


class Client(metaclass=SingletonMeta):
    conn = None

    def connect(self, host, port, username, password, db_name):
        self.db_name = db_name

        self.conn = MongoClient(host='{}:{}'.format(
            host, port), username=username, password=password)

    def getDB(self):
        return self.conn[self.db_name]
