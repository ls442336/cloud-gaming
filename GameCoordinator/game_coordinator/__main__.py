import asyncio
from autobahn.asyncio.websocket import WebSocketServerFactory
from game_coordinator.game_coordinator import Connection
from game_coordinator.database import Client
from dotenv import load_dotenv, find_dotenv
from game_coordinator.logger import logger
import logging
import os

load_dotenv(find_dotenv())

SERVER_ID = os.environ.get('SERVER_ID')
SERVER_PORT = os.environ.get('PORT')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

if __name__ == '__main__':
    # Register routes
    logger.info('Registrando as rotas')

    # Connect Database
    logger.info(
        'Criando conexão com o banco de dados {}:{}'.format(DB_HOST, DB_PORT))
    client = Client()
    client.connect(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE)

    # Clean data
    logger.info('Apagando dados anteriores')
    db = client.getDB()

    logger.info('Limpando sessões')
    db.sessions.update_many({
        'server_id': {
            '$eq': SERVER_ID
        },
        'active': {
            '$eq': True
        }
    },
        {
        '$set': {
            'status': 'ended',
            'active': False
        }
    })

    logger.info('Limpando instâncias')
    db.instances.update_many({
        'server_id': {
            '$eq': SERVER_ID
        },
        'active': {
            '$eq': True
        }
    }, {
        '$set': {
            'active': False
        }
    })

    logger.info('Limpando usuários')
    db.users.update_many({
        'server_id': {
            '$eq': SERVER_ID
        },
        'active': {
            '$eq': True
        }
    }, {
        '$set': {
            'active': False
        }
    })

    # Start server
    logger.info('Iniciando o servidor')
    factory = WebSocketServerFactory()
    factory.protocol = Connection

    logger.info('Servidor iniciado na porta {}'.format(SERVER_PORT))

    loop = asyncio.get_event_loop()
    coro = loop.create_server(factory, '127.0.0.1', SERVER_PORT)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        loop.close()
