from autobahn.asyncio.websocket import WebSocketServerProtocol
from game_coordinator.repositories import ConnectionRepository
from game_coordinator.entities import ConnectionEntity
from game_coordinator.logger import logger
import logging
import json
import os
from game_coordinator.database import Client
from bson.objectid import ObjectId

logger = logging.getLogger('Connection')
connRepository = ConnectionRepository()
client = Client()


class Connection(WebSocketServerProtocol):
    controller = None

    def onConnect(self, request):
        logger.info('Conexão feita {}'.format(request.peer))

        self.peer = request.peer

        self.conn = ConnectionEntity(self)
        connRepository.add(self.conn)

        self.routes = {}
        self.routes['register_user'] = self.route_register_user
        self.routes['register_instance'] = self.route_register_instance
        self.routes['users/start_session'] = self.route_start_session
        self.routes['gaming_instance/ready'] = self.route_instance_ready
        self.routes['gaming_instance/confirm_session'] = self.route_confirm_session
        self.routes['users/get_answer'] = self.route_get_answer
        self.routes['gaming_instance/answer'] = self.route_answer
        self.routes['users/answer_received'] = self.route_answer_received
        self.routes['gaming_instance/download_done'] = self.route_download_done
        self.routes['gaming_instance/download_error'] = self.route_download_error
        self.routes['gaming_instance/game_openned'] = self.game_openned
        self.routes['gaming_instance/game_open_error'] = self.game_open_error

    def route_download_done(self, payload):
        # TODO: validar payload
        db = client.getDB()

        session = db.sessions.find_one({
            'instance': {
                '$eq': ObjectId(payload['instance'])
            },
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(str(session['_id']))
            }, {
                '$set': {
                    'status': 'openning_game'
                }
            })

            user = db.users.find_one({
                '_id': ObjectId(str(session['user']))
            })

            if user is None:  # TODO: ?
                logger.error('Usuário não encontrado')
                return

            instance = db.instances.find_one({
                '_id': ObjectId(str(session['instance']))
            })

            if instance is None:  # TODO: ?
                logger.error('Instância não encontrada')
                return

            conn_user = connRepository.findById(user['conn_id'])

            conn_instance = connRepository.findById(instance['conn_id'])

            if conn_user is None:
                logger.warning('Conexão do usuário não encontrada')
                return

            if conn_instance is None:
                logger.warning('Conexão da instância não encontrada')
                return

            conn_user.conn.send({
                'type': 'status',
                'status': 'openning_game'
            })

            conn_instance.conn.send({
                'type': 'action',
                'action': 'open_game'
            })

    def route_download_error(self, payload):
        pass

    def game_openned(self, payload):
        # TODO: validar payload
        db = client.getDB()

        session = db.sessions.find_one({
            'instance': {
                '$eq': ObjectId(payload['instance'])
            },
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(str(session['_id']))
            }, {
                '$set': {
                    'status': 'streaming'
                }
            })

            user = db.users.find_one({
                '_id': ObjectId(str(session['user']))
            })

            if user is None:  # TODO: ?
                logger.error('Usuário não encontrado')
                return

            instance = db.instances.find_one({
                '_id': ObjectId(str(session['instance']))
            })

            if instance is None:  # TODO: ?
                logger.error('Instância não encontrada')
                return

            conn_user = connRepository.findById(user['conn_id'])
            conn_instance = connRepository.findById(instance['conn_id'])

            if conn_user is None:
                logger.warning('Conexão do usuário não encontrada')
                return

            if conn_instance is None:
                logger.warning('Conexão da instância não encontrada')
                return

            conn_user.conn.send({
                'type': 'status',
                'status': 'streaming'
            })

            conn_instance.conn.send({
                'type': 'action',
                'action': 'stream'
            })

    def game_open_error(self, payload):
        pass

    def route_answer_received(self, payload):
        db = client.getDB()

        session = db.sessions.find_one({
            '_id': ObjectId(payload['session_id']),
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(payload['session_id'])
            }, {
                '$set': {
                    'status': 'downloading_game'
                }
            })

            instance = db.instances.find_one({
                '_id': ObjectId(str(session['instance']))
            })

            instance_conn = connRepository.findById(instance['conn_id'])

            instance_conn.conn.send({
                'type': 'action',
                'action': 'download_game'
            })

            user = db.users.find_one({
                '_id': ObjectId(str(session['user']))
            })

            user_conn = connRepository.findById(user['conn_id'])

            user_conn.conn.send({
                'type': 'status',
                'status': 'downloading_game'
            })

    def route_answer(self, payload):
        db = client.getDB()

        session = db.sessions.find_one({
            '_id': ObjectId(payload['session_id']),
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(payload['session_id'])
            }, {
                '$set': {
                    'status': 'waiting_offer_confirmation'
                }
            })

            user = db.users.find_one({
                '_id': ObjectId(str(session['user']))
            })

            user_conn = connRepository.findById(user['conn_id'])

            user_conn.conn.send({
                'type': 'action',
                'action': 'answer',
                'session_id': str(session['_id']),
                'answer': payload['answer']
            })

    def route_get_answer(self, payload):
        db = client.getDB()

        session = db.sessions.find_one({
            '_id': ObjectId(payload['session_id']),
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(payload['session_id'])
            }, {
                '$set': {
                    'status': 'waiting_answer'
                }
            })

            instance = db.instances.find_one({
                '_id': ObjectId(str(session['instance']))
            })

            instance_conn = connRepository.findById(instance['conn_id'])

            instance_conn.conn.send({
                'type': 'action',
                'action': 'get_answer',
                'offer': payload['offer']
            })

    def route_confirm_session(self, payload):
        db = client.getDB()

        session = db.sessions.find_one({
            '_id': ObjectId(payload['session_id']),
            'active': {
                '$eq': True
            }
        })

        if session is not None:
            db.sessions.update_one({
                '_id': ObjectId(payload['session_id'])
            }, {
                '$set': {
                    'instance': ObjectId(payload['instance']),
                    'status': 'waiting_offer'
                }
            })

            user = db.users.find_one({
                '_id': ObjectId(str(session['user']))
            })

            user_conn = connRepository.findById(user['conn_id'])

            user_conn.conn.send({
                'type': 'action',
                'action': 'get_offer',
                'session_id': str(session['_id'])
            })

    def route_instance_ready(self, payload):
        db = client.getDB()

        db.instances.update_one({
            '_id': ObjectId(payload['instance'])
        }, {
            '$set': {
                'ready': True
            }
        })

    def route_register_user(self, payload):
        SERVER_ID = os.environ.get('SERVER_ID')

        db = client.getDB()

        user = db.users.insert_one({
            'conn_id': str(self.conn.id),
            'server_id': str(SERVER_ID),
            'active': True
        })

        self.send({
            'type': 'status',
            'status': 'register_success',
            'user': str(user.inserted_id)
        })

    def route_register_instance(self, payload):
        SERVER_ID = os.environ.get('SERVER_ID')

        db = client.getDB()

        instance = db.instances.insert_one({
            'conn_id': str(self.conn.id),
            'server_id': str(SERVER_ID),
            'ready': False,
            'active': True
        })

        self.send({
            'type': 'status',
            'status': 'register_success',
            'instance': str(instance.inserted_id)
        })

    def route_start_session(self, payload):
        # TODO: validar se o usuário é o mesmo
        # TODO: validar se o jogo existe

        self.send({
            'type': 'status',
            'status': 'searching_instance'
        })

        SERVER_ID = os.environ.get('SERVER_ID')
        db = client.getDB()

        # Busca o jogo

        game = db.games.find_one({
            '_id': ObjectId(payload['game'])
        })

        if game is None:
            self.send({
                'type': 'status',
                'status': 'game_not_found'
            })

            raise Exception(
                'Jogo não encontrado {}'.format(payload['game']))

        # Procura uma instância livre
        instance = db.instances.find_one({
            'server_id': {
                '$eq': SERVER_ID
            },
            'ready': {
                '$eq': True
            },
            'active': {
                '$eq': True
            }
        })

        if instance is None:
            self.send({
                'type': 'status',
                'status': 'no_instances_available'
            })
        else:
            # Cria a sessão
            session_result = None

            session_result = db.sessions.insert_one({
                'game': ObjectId(str(game['_id'])),
                'user': ObjectId(payload['user']),
                'server_id': SERVER_ID,
                'status': 'searching_instance',
                'active': True
            })

            if session_result is None:
                raise Exception('Não foi possível criar uma sessão')

            session_inserted_id = str(session_result.inserted_id)

            session = db.sessions.find_one({
                '_id': ObjectId(session_inserted_id)
            })

            db.instances.update_one({
                '_id': ObjectId(str(instance['_id']))
            }, {
                '$set': {
                    'ready': False
                }
            })

            self.send({
                'type': 'status',
                'status': 'instance_found'
            })

            instance_conn = connRepository.findById(instance['conn_id'])

            print('DEBUG____', instance_conn)

            instance_conn.conn.send({
                'type': 'action',
                'action': 'start_session',
                'session': {
                    'id': str(session['_id']),
                    'game': {
                        'id': str(game['_id']),
                        'bucket_id': game['bucket_id'],
                        'path': game['path']
                    }
                }
            })

    def onMessage(self, payload, isBinary):
        logger.info('Mensagem recebida de {}'.format(self.peer))
        logger.info("Payload: " + payload.decode('utf-8'))

        try:
            data = json.loads(payload.decode('utf8'))

            logger.info(data)

            try:
                print(data)
                self.routes[data['route']](data)
            except Exception as e:
                logger.error('Chamar rota: ' + data['route'] + ' ' + str(e))
        except Exception as e:
            logger.error('Parse JSON: ' + str(e))

    def send(self, payload):
        logger.info('Mensagem enviada para {}'.format(self.peer))

        try:
            data = json.dumps(payload, ensure_ascii=False).encode('utf8')
            self.sendMessage(data, False)
        except Exception as e:
            logger.error(e)

    def onClose(self, wasClean, code, reason):
        # Limpar o que precisar
        db = client.getDB()

        user = db.users.find_one({
            'conn_id': {
                '$eq': self.conn.id,
            },
            'active': {
                '$eq': True
            }
        })

        if user is not None:
            db.users.update_one({
                '_id': ObjectId(user['_id'])
            }, {
                '$set': {
                    'active': False
                }
            })

            session = db.sessions.find_one({
                'user': {
                    '$eq': ObjectId(user['_id']),
                },
                'active': {
                    '$eq': True
                }
            })

            if session is not None:
                db.sessions.update_one({
                    '_id': ObjectId(session['_id'])
                }, {
                    '$set': {
                        'status': 'ended',
                        'active': False
                    }
                })

                instance = db.instances.find_one({
                    '_id': ObjectId(session['instance'])
                })

                if instance is not None:
                    conn_instance = connRepository.findById(
                        instance['conn_id'])

                    if conn_instance is not None:
                        conn_instance.conn.send({
                            'type': 'action',
                            'action': 'end_session'
                        })
        else:
            instance = db.instances.find_one({
                'conn_id': {
                    '$eq': self.conn.id,
                },
                'active': {
                    '$eq': True
                }
            })

            if instance is not None:
                db.instances.update_one({
                    '_id': ObjectId(instance['_id'])
                }, {
                    '$set': {
                        'active': False
                    }
                })

                session = db.sessions.find_one({
                    'instance': {
                        '$eq': ObjectId(instance['_id']),
                    },
                    'active': {
                        '$eq': True
                    }
                })

                if session is not None:
                    db.sessions.update_one({
                        '_id': ObjectId(session['_id'])
                    }, {
                        '$set': {
                            'status': 'ended',
                            'active': False
                        }
                    })

                    user = db.users.find_one({
                        '_id': ObjectId(session['user'])
                    })

                    if user is not None:
                        conn_instance = connRepository.findById(
                            user['conn_id'])

                        if conn_instance is not None:
                            conn_instance.conn.send({
                                'type': 'status',
                                'status': 'session_ended'
                            })

        connRepository.remove(self.conn)
