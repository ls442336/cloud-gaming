from game_coordinator.entity import Entity


class ConnectionEntity(Entity):
    def __init__(self, conn):
        Entity.__init__(self)

        self.conn = conn
