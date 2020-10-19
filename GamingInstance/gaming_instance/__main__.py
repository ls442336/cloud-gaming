from dotenv import load_dotenv, find_dotenv
from gaming_instance.application import Application
import sys
import asyncio

load_dotenv(find_dotenv())

asyncio.get_event_loop().close()

if __name__ == '__main__':
    app = Application()
    app.init()
    app.mainloop()
