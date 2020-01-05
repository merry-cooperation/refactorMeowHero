import unittest
from unittest import TestCase
from unittest.mock import patch
from modules.interface import Button


class TestButtonDataClump(TestCase):
    @patch('modules.interface.pygame.transform.scale')
    @patch('modules.interface.pygame.image.load')
    @patch('modules.interface.pygame.font.SysFont')
    def setUp(self, mock_sys_font, mock_image_load, mock_transform_scale):
        self.button = Button(1, 2, 10, 20)
        self.mock_sys_font = mock_sys_font
        self.mock_image_load = mock_image_load
        self.mock_transform_scale = mock_transform_scale

    def test_init_calls_pygame_font_SysFont_once(self):
        self.mock_sys_font.assert_called_once()

    def test_init_calls_pygame_image_load_3times(self):
        self.assertEqual(self.mock_image_load.call_count, 3)

    def test_init_calls_pygame_transform_scale_3times(self):
        self.assertEqual(self.mock_transform_scale.call_count, 3)

    def test_init_sets_x(self):
        self.assertEqual(self.button.x, 1)

    def test_init_sets_y(self):
        self.assertEqual(self.button.y, 2)

    def test_init_sets_w(self):
        self.assertEqual(self.button.w, 10)

    def test_init_sets_h(self):
        self.assertEqual(self.button.h, 20)

    def test_init_passing_wh_to_pygame_transform_scale(self):
        for call_args in self.mock_transform_scale.call_args_list:
            with self.subTest(call_args=call_args):
                self.assertEqual(call_args[0][1], (self.button.w, self.button.h))


def main():
    unittest.main()


if __name__ == "__main__":
    main()
