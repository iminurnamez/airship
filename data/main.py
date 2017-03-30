from . import prepare,tools
from .states import title_screen, gameplay, level_fail, level_win, level_editor, level_select, level_edit_select, help_screen


def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {"TITLE": title_screen.TitleScreen(),
                   "GAMEPLAY": gameplay.Gameplay(),
                   "LEVELFAIL": level_fail.LevelFailScreen(),
                   "LEVELWIN": level_win.LevelWinScreen(),
                   "LEVELEDITOR": level_editor.LevelEditor(),
                   "LEVELSELECT": level_select.LevelSelect(),
                   "LEVELEDITSELECT": level_edit_select.LevelEditSelect(),
                   "HELPSCREEN": help_screen.HelpScreen()}
    controller.setup_states(states, "TITLE")
    controller.main()
