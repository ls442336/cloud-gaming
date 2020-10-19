import sys

sys.path.append('../')

from gaming_instance.connection import ConnectionManager

connManager = ConnectionManager()

connManager.getConnection().send('oi')
connManager.getConnection().send('oi')