from game_coordinator.singleton import SingletonMeta


class Repository:
    def __init__(self):
        self.entities = []

    def add(self, entity):
        self.entities.append(entity)

        return entity

    def remove(self, entity):
        try:
            self.entities.remove(entity)
        except Exception as e:
            print(e)
            return None

        return entity

    def findById(self, id):
        for ent in self.entities:
            if ent.id == id:
                return ent

        return None
