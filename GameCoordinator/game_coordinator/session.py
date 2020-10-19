from enum import Enum


class Role(Enum):
    NONE = 0
    GAMING_INSTANCE = 1
    PLAYER = 2


class Session:
    def __init__(self):
        self.id = None
        self.conn_id = None
        self.role = Role.NONE
