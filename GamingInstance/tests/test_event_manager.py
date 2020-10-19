import unittest

from gaming_instance.event_manager import EventManager

test_emit_value = 0

def change_emit_value():
    global test_emit_value

    test_emit_value = 1

class TestEventManager(unittest.TestCase):
    def test_on(self):
        eventManager = EventManager()
        eventName = 'teste'

        eventManager.on(eventName, lambda x: x)

        self.assertIn(eventName, eventManager.listeners)

    def test_emit(self):
        eventManager = EventManager()
        eventName = 'teste'

        eventManager.on(eventName, lambda x: change_emit_value())
        eventManager.emit(eventName, 1)

        self.assertEqual(test_emit_value, 1)

if __name__ == '__main__':
    unittest.main()
