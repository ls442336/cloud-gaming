import sys
sys.path.insert(1, '../')


def test():
    from game_coordinator.entity import Entity

    ent1 = Entity()
    ent2 = Entity()

    print(ent1.id)
    print(ent2.id)


test()
