import unittest
from unittest import TestCase
from unittest.mock import patch
from modules.interface import Button


@patch('modules.interface.pygame.transform.scale')
@patch('modules.interface.pygame.image.load')
@patch('modules.interface.pygame.font.SysFont')
class TestButton(TestCase):

    def test_init_calls_pygame_font_SysFont_once(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        mock_sys_font.assert_called_once()

    def test_init_calls_pygame_image_load_3times(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(mock_image_load.call_count, 3)

    def test_init_calls_pygame_transform_scale_3times(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(mock_transform_scale.call_count, 3)

    def test_init_sets_x(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(button.x, 1)

    def test_init_sets_y(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(button.y, 2)

    def test_init_sets_w(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(button.w, 10)

    def test_init_sets_h(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        self.assertEqual(button.h, 20)

    def test_init_passing_wh_to_pygame_transform_scale(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)
        for call_args in mock_transform_scale.call_args_list:
            with self.subTest(call_args=call_args):
                self.assertEqual(call_args[0][1], (button.w, button.h))

    def test_is_over_mouse_pos_inside_button(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((5, 5))
        self.assertTrue(mouse_is_over_button)
        self.assertTrue(button.is_active)

    def test_is_over_mouse_pos_outside_button(self, mock_sys_font, mock_image_load, mock_transform_scale):
        button = Button(1, 2, 10, 20)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((0, 0))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_x_too_low(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((0, 10))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_x_too_high(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((20, 10))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_y_too_low(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((10, 0))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_y_too_high(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((10, 20))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_x_at_lower_edge_minus_one(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((5, 10))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_x_at_upper_edge_plus_one(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((15, 10))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_y_at_lower_edge_minus_one(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((10, 5))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)

    def test_is_over_y_at_upper_edge_plus_one(self, mock_sys_font, mock_image_load, mock_transform_scale):
        # button rect top left (5,5) bottom right (15,15)
        button = Button(5, 5, 10, 10)

        self.assertFalse(button.is_active)
        mouse_is_over_button = button.is_over((10, 15))
        self.assertFalse(mouse_is_over_button)
        self.assertFalse(button.is_active)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
