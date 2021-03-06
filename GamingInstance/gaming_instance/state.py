from enum import Enum


class State(Enum):
    NONE = 0
    START_CONNECTION = 1
    RETRY_CONNECTION = 2
    REGISTER = 3
    CONNECTION_LOST = 4
    WAITING_REGISTRATION = 5
    IDLE = 6
    WAITING_OFFER = 7
    WAITING_ANSWER_CONFIRMATION = 8
    END_SESSION = 9
    STREAMING = 10
    OPENNING_GAME = 11
    DOWNLOADING_GAME = 12
    WAITING_SESSION_TO_END = 13
    DOWNLOAD_DONE = 14
    WAITING_TO_STREAM = 15
    WAITING_ANSWER = 16
    WAITING_DOWNLOAD_END_SESSION = 17
