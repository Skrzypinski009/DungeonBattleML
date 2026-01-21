import unittest
from models import Actor, ActorType


class ActorModelTest(unittest.TestCase):
    def test_create(self):
        actor_type = ActorType.create(
            name="TestActor", max_health=5, max_energy=1, attack_damage=2
        )
        actor = Actor.create(type=actor_type, health=2, energy=1)

        self.assertEqual(actor.health, 2)
        self.assertEqual(actor.energy, 1)
        self.assertEqual(actor.type, actor_type)


if __name__ == "__main__":
    unittest.main()
