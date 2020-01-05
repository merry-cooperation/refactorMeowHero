import unittest
from unittest import TestCase
from modules.game import enemy_switch_by_level
from modules.objects import Children, Dog, DancingCat, CatBossEnemy


class TestEnemySwitchByLevel(TestCase):

    def test_level_number_2_returns_children(self):
        enemy = enemy_switch_by_level(2)
        self.assertIsInstance(enemy, Children)

    def test_level_number_3_returns_dog(self):
        enemy = enemy_switch_by_level(3)
        self.assertIsInstance(enemy, Dog)

    def test_level_number_8_returns_dog(self):
        enemy = enemy_switch_by_level(8)
        self.assertIsInstance(enemy, DancingCat)

    def test_level_number_11_returns_dog(self):
        enemy = enemy_switch_by_level(11)
        self.assertIsInstance(enemy, CatBossEnemy)

    def test_level_number_1_returns_none(self):
        enemy = enemy_switch_by_level(1)
        self.assertIsNone(enemy)

    def test_level_number_4_returns_none(self):
        enemy = enemy_switch_by_level(4)
        self.assertIsNone(enemy)

    def test_level_number_5_returns_none(self):
        enemy = enemy_switch_by_level(5)
        self.assertIsNone(enemy)

    def test_level_number_6_returns_none(self):
        enemy = enemy_switch_by_level(6)
        self.assertIsNone(enemy)

    def test_level_number_7_returns_none(self):
        enemy = enemy_switch_by_level(7)
        self.assertIsNone(enemy)

    def test_level_number_9_returns_none(self):
        enemy = enemy_switch_by_level(9)
        self.assertIsNone(enemy)

    def test_level_number_10_returns_none(self):
        enemy = enemy_switch_by_level(10)
        self.assertIsNone(enemy)

    def test_level_number_12_returns_none(self):
        enemy = enemy_switch_by_level(12)
        self.assertIsNone(enemy)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
