from game_coordinator.singleton import SingletonMeta


class Repository(metaclass=SingletonMeta):
    entities = []

    def add(self, entity):
        self.entities.append(entity)

    def findById(self, id):
        for e in self.entities:
            if e.id == id:
                return e

        return None

    def remove(self, entity):
        ent = self.findById(entity.id)

        if ent is not None:
            self.entities.remove(entity)

        return ent
