from dotenv import load_dotenv, find_dotenv
import os
import time

load_dotenv(find_dotenv('.env.test'))


def test():
    import sys
    sys.path.append('../')
    from gaming_instance.game_downloader import GameDownloader
    from gaming_instance.game_downloader import State

    game_folder = os.environ.get("GAMES_FOLDER")
    game_path = "IronSnoutGamejolt\\IronSnout.exe"

    path = os.path.join(game_folder, game_path)

    downloader = GameDownloader()
    downloader.download('cloud-test-bucket-0001',
                        'gameid.zip', 'C:\\Users\\Lucas\\Downloads\\download.zip')

    while downloader.getDownload().status == State.DOWNLOADING:
        print('baixando')

    print('baixou')

    # print('torresmo')

    # time.sleep(2)

    # manager.close()


test()
