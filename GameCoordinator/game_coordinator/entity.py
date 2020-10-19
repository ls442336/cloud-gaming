class Entity:
    __id = 0

    def __init__(self):
        self.id = str(Entity.__id)
        Entity.__id += 1
