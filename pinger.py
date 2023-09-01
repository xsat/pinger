from configparser import ConfigParser
from hashlib import md5
from PySimpleGUI import theme, rgb, theme_element_background_color, Window, Text, StatusBar, Button, Element, WIN_CLOSED
from ping import ping
from time import strftime


DEFAULT_THEME: str = 'Dark'

SETTINGS_FILENAME: str = 'data/settings.ini'
TRANSLATION_FILENAME: str = 'data/translation.ini'

DEFAULT_LANGUAGE: str = 'DEFAULT'

BLACK_COLOR: str = rgb(0, 0, 0)
RED_COLOR: str = rgb(200, 0, 0)
GREEN_COLOR: str = rgb(0, 200, 0)
BLUE_COLOR: str = rgb(0, 87, 183)
YELLOW_COLOR: str = rgb(255, 215, 0)

TEST_BUTTON_KEY: str = 'TEST_BUTTON'
CLOSE_BUTTON_KEY: str = 'CLOSE_BUTTON'
LAST_CHECK_TEXT_KEY: str = 'LAST_CHECK_TEXT'
WINDOW_TITLE_KEY: str = 'WINDOW_TITLE'

DEFAULT_LAST_CHECK_TEXT: str = '0000-00-00 00:00:00'
DEFAULT_TIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'


def pinger() -> None:
    def generate_key(left_name: str, right_name: str) -> str:
        return md5(f'{left_name}-{right_name}'.encode()).hexdigest()

    def get_background_color(is_success_status: bool) -> str:
        if is_success_status:
            return GREEN_COLOR

        return RED_COLOR

    def get_last_check_text() -> str:
        return strftime(DEFAULT_TIME_FORMAT)

    theme(DEFAULT_THEME)

    layout: list[list[Element]] = []
    element_keys: list[str] = []

    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        layout.append([Text(section_name)])

        for value_name in config[section_name]:
            element_key = generate_key(section_name, value_name)
            element_keys.append(element_key)
            layout.append([StatusBar(value_name, key=element_key, metadata=config[section_name][value_name])])

    config.read(TRANSLATION_FILENAME)

    selected_language: str = DEFAULT_LANGUAGE

    layout.append([
        Button(config[selected_language][TEST_BUTTON_KEY], key=TEST_BUTTON_KEY, button_color=BLUE_COLOR),
        Button(config[selected_language][CLOSE_BUTTON_KEY], key=CLOSE_BUTTON_KEY, button_color=YELLOW_COLOR),
        Text(DEFAULT_LAST_CHECK_TEXT, key=LAST_CHECK_TEXT_KEY)])

    window: Window = Window(config[selected_language][WINDOW_TITLE_KEY], layout, resizable=True)
    default_element_background_color: str = theme_element_background_color()

    while True:
        event, _ = window.read()

        if event == WIN_CLOSED or event == CLOSE_BUTTON_KEY:
            break

        if event == TEST_BUTTON_KEY:
            for element_key in element_keys:
                window[element_key].update(background_color=default_element_background_color)

            last_check_text: str = get_last_check_text()
            window[LAST_CHECK_TEXT_KEY].update(value=last_check_text)
            window.refresh()

            for element_key in element_keys:
                address: str = window[element_key].metadata
                is_ping_success: bool = ping(address)
                new_background_color: str = get_background_color(is_ping_success)
                window[element_key].update(background_color=new_background_color)
                window.refresh()

    window.close()


if __name__ == '__main__':
    pinger()
