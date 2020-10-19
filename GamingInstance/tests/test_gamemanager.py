from dotenv import load_dotenv, find_dotenv
import os
import time

load_dotenv(find_dotenv('.env.test'))


def test():
    import sys
    sys.path.append('../')
    from gaming_instance.game_manager import GameManager

    game_folder = os.environ.get("GAMES_FOLDER")
    game_path = "IronSnoutGamejolt\\IronSnout.exe"

    path = os.path.join(game_folder, game_path)

    manager = GameManager()
    game_pid = manager.open(path)

    # print('torresmo')

    # time.sleep(2)

    # manager.close()


test()
