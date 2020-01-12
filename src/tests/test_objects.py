import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
import pygame
from modules.objects import MeowHero, Health, Bullet


@patch('modules.objects.pygame.transform.scale', autospec=True)
@patch('modules.objects.pygame.image.load', autospec=True)
class TestMeowHero(TestCase):

    def test_init_calls_pygame_image_load_2times(self, mock_image_load, mock_transform_scale):
        meow_hero = MeowHero(1)
        self.assertEqual(mock_image_load.call_count, 2)

    def test_init_calls_pygame_transform_scale_2times(self, mock_image_load, mock_transform_scale):
        meow_hero = MeowHero(1)
        self.assertEqual(mock_transform_scale.call_count, 2)

    def test_init_calls_get_rect_2times(self, mock_image_load, mock_transform_scale):
        mock_get_rect = Mock()
        mock_transform_scale.return_value.get_rect = mock_get_rect

        meow_hero = MeowHero(1)
        self.assertEqual(mock_get_rect.call_count, 2)


@patch('modules.objects.pygame.transform.scale', autospec=True)
@patch('modules.objects.pygame.image.load', autospec=True)
class TestHealth(TestCase):

    def test_init_calls_pygame_image_load_once(self, mock_image_load, mock_transform_scale):
        health = Health(1, 10, 10)
        mock_image_load.assert_called_once()

    def test_init_calls_pygame_transform_scale_once(self, mock_image_load, mock_transform_scale):
        health = Health(1, 10, 10)
        mock_transform_scale.assert_called_once()

    def test_init_calls_get_rect_once(self, mock_image_load, mock_transform_scale):
        mock_get_rect = Mock()
        mock_transform_scale.return_value.get_rect = mock_get_rect

        health = Health(1, 10, 10)
        mock_get_rect.assert_called_once()


@patch('modules.objects.pygame.transform.scale', autospec=True)
@patch('modules.objects.pygame.image.load', autospec=True)
class TestBullet(TestCase):

    def test_init_simple_calls_pygame_image_load_once(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Simple")
        mock_image_load.assert_called_once()

    def test_init_simple_calls_pygame_transform_scale_once(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Simple")
        mock_transform_scale.assert_called_once()

    def test_init_simple_calls_get_rect_once(self, mock_image_load, mock_transform_scale):
        mock_get_rect = Mock()
        mock_transform_scale.return_value.get_rect = mock_get_rect

        bullet = Bullet(1, "Simple")
        mock_get_rect.assert_called_once()

    def test_init_multiplayer_calls_pygame_image_load_once(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Multiplayer")
        mock_image_load.assert_called_once()

    def test_init_multiplayer_calls_pygame_transform_scale_once(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Multiplayer")
        mock_transform_scale.assert_called_once()

    def test_init_multiplayer_calls_get_rect_once(self, mock_image_load, mock_transform_scale):
        mock_get_rect = Mock()
        mock_transform_scale.return_value.get_rect = mock_get_rect

        bullet = Bullet(1, "Multiplayer")
        mock_get_rect.assert_called_once()

    def test_bullet_image_raises_attribute_error(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Simple")
        self.assertTrue(hasattr(bullet, 'image'))

    def test_bullet_isinstance_pygame_sprite(self, mock_image_load, mock_transform_scale):
        bullet = Bullet(1, "Simple")
        self.assertIsInstance(bullet, pygame.sprite.Sprite)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
