from os import path
from hashlib import md5
from configparser import ConfigParser
from PySimpleGUI import Text, StatusBar, Button, Element, Window
from pinger.restore_elements import LAST_CHECK_TEXT_KEY
from pinger.colors import BLUE_COLOR, YELLOW_COLOR

DATA_FILENAME: str = path.abspath('data/data.ini')
TRANSLATION_FILENAME: str = path.abspath('data/translation.ini')

ICON_FILENAME = path.abspath('data/icon.ico')

DEFAULT_LANGUAGE: str = 'DEFAULT'

TEST_BUTTON_KEY: str = 'TEST_BUTTON'
CLOSE_BUTTON_KEY: str = 'CLOSE_BUTTON'
WINDOW_TITLE_KEY: str = 'WINDOW_TITLE'

DEFAULT_LAST_CHECK_TEXT: str = '0000-00-00 00:00:00'


def create_window_and_element_keys() -> tuple[Window, list[str]]:
    def generate_key(left_name: str, right_name: str) -> str:
        return md5(f'{left_name}-{right_name}'.encode()).hexdigest()

    layout: list[list[Element]] = []
    element_keys: list[str] = []

    config: ConfigParser = ConfigParser()
    config.read(DATA_FILENAME)

    for section_name in config.sections():
        layout.append([Text(section_name)])

        for value_name in config[section_name]:
            element_key = generate_key(section_name, value_name)
            element_keys.append(element_key)
            layout.append([StatusBar(value_name, key=element_key,
                                     metadata=config[section_name][value_name])])

    config.read(TRANSLATION_FILENAME)

    selected_language: str = DEFAULT_LANGUAGE

    layout.append([
        Button(config[selected_language][TEST_BUTTON_KEY], key=TEST_BUTTON_KEY, button_color=BLUE_COLOR),
        Button(config[selected_language][CLOSE_BUTTON_KEY], key=CLOSE_BUTTON_KEY, button_color=YELLOW_COLOR),
        Text(DEFAULT_LAST_CHECK_TEXT, key=LAST_CHECK_TEXT_KEY)])

    window: Window = Window(config[selected_language][WINDOW_TITLE_KEY], layout, icon=ICON_FILENAME, resizable=True)

    return window, element_keys
