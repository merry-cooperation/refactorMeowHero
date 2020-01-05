import unittest
from unittest import TestCase
from unittest.mock import patch, Mock
import pygame
from modules.layouts import create_profile_layout
from modules.interface import Player


@patch('modules.layouts.interface.create_empty_profile')
@patch('modules.layouts.os.path.isfile')
@patch('modules.layouts.interface.load_player_by_path')
@patch('modules.layouts.pygame.mouse.get_pos')
@patch('modules.layouts.pygame.display.update')
@patch('modules.layouts.pygame.draw.rect')
@patch('modules.layouts.pygame.event.get')
@patch('modules.layouts.interface.InputBox')
@patch('modules.layouts.pygame.font.SysFont')
class TestCreateProfileLayout(TestCase):
    def test_load_existing_player_by_mouse_click(
            self, mock_sys_font, mock_input_box, mock_event_get,
            mock_draw_rect, mock_display_update, mock_mouse_get_pos,
            mock_load_player_by_path, mock_os_path_isfile, mock_create_empty_profile
    ):
        mock_event_get.return_value = [pygame.event.Event(pygame.MOUSEBUTTONDOWN)]
        mock_mouse_get_pos.return_value = (1070, 470)
        mock_input_box.return_value.text = 'Oleg'
        mock_os_path_isfile.return_value = True

        expected_player = Player('Oleg', 100, [1, 2, 3], [1, 2], 1)
        mock_load_player_by_path.return_value = expected_player

        mock_window_surface = Mock()
        mock_player = Mock()
        player = create_profile_layout(mock_window_surface, mock_player, 1600, 900)

        self.assertEqual(player.name, expected_player.name)
        self.assertEqual(player.score, expected_player.score)
        self.assertEqual(player.levels, expected_player.levels)
        self.assertEqual(player.skins, expected_player.skins)
        self.assertEqual(player.current_skin, expected_player.current_skin)

    def test_create_and_load_new_player_by_mouse_click(
            self, mock_sys_font, mock_input_box, mock_event_get,
            mock_draw_rect, mock_display_update, mock_mouse_get_pos,
            mock_load_player_by_path, mock_os_path_isfile, mock_create_empty_profile
    ):
        mock_event_get.return_value = [pygame.event.Event(pygame.MOUSEBUTTONDOWN)]
        mock_mouse_get_pos.return_value = (1070, 470)
        mock_input_box.return_value.text = 'Oleg'
        mock_os_path_isfile.return_value = False

        expected_player = Player('Oleg', 0, [1], [1], 1)
        mock_load_player_by_path.return_value = expected_player

        mock_window_surface = Mock()
        mock_player = Mock()
        player = create_profile_layout(mock_window_surface, mock_player, 1600, 900)

        self.assertEqual(player.name, expected_player.name)
        self.assertEqual(player.score, expected_player.score)
        self.assertEqual(player.levels, expected_player.levels)
        self.assertEqual(player.skins, expected_player.skins)
        self.assertEqual(player.current_skin, expected_player.current_skin)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
