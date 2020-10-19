from enum import Enum
from threading import Thread
import boto3
import botocore
from gaming_instance.logger import logger
import logging

s3 = boto3.resource('s3')


class State(Enum):
    NONE = 0
    DOWNLOADING = 1
    DONE = 2
    ERROR = 3


class GameDownloader:

    instance = None

    def download(self, bucketName, objectId, path):
        if self.instance is not None:
            raise Exception('Já existe um download em andamento')

        self.instance = DownloadInstance(bucketName, objectId, path)
        self.instance.start()

        return self.instance

    def getDownload(self):
        return self.instance

    def clear(self):
        self.instance = None


class DownloadInstance(Thread):

    status = State.NONE

    def __init__(self, bucketName, objectId, path):
        Thread.__init__(self)

        self.bucketName = bucketName
        self.objectId = objectId
        self.path = path

        self.logger = logging.getLogger('DownloadInstance')

    def run(self):
        self.status = State.DOWNLOADING

        try:
            self.logger.info('Download iniciado:\nbucket_name: {}\nobject_id: {}\npath: {}'.format(
                self.bucketName, self.objectId, self.path))

            s3.Bucket(self.bucketName).download_file(
                self.objectId, self.path)
            self.status = State.DONE
        except Exception as e:
            self.logger.error(e)
            self.status = State.ERROR
