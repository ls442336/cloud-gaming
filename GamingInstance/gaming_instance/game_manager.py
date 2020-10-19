import subprocess
import os
import signal
import psutil
import time


class GameManager:
    target = None

    def open(self, path):
        parent = subprocess.Popen(path, shell=True)
        process = psutil.Process(parent.pid)

        startTime = time.time()

        while len(process.children(recursive=False)) == 0:
            if time.time() - startTime > 60:
                raise 'Jogo demorou demais para abrir'

        self.target = process.children(recursive=False)[0]

        time.sleep(5)

        subprocess.run(args=['./utils/Injector.exe', '-i', '-p',
                             str(self.target.pid), 'screenrecorder.dll'])

        return self.target

    def close(self):
        if self.target is None:
            raise 'target é None'

        self.target.kill()

    def getStatus(self):
        if self.target is not None:
            return self.target.status()
        else:
            raise Exception('target é None')
