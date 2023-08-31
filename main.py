from configparser import ConfigParser
from hashlib import md5
from PySimpleGUI import theme, rgb, theme_element_background_color, Window, Text, StatusBar, Button, Element, WIN_CLOSED
from ping import ping
from time import strftime

DEFAULT_THEME: str = 'Dark'

SETTINGS_FILENAME: str = 'settings.ini'

BLACK_COLOR: str = rgb(0, 0, 0)
RED_COLOR: str = rgb(255, 0, 0)
GREEN_COLOR: str = rgb(0, 255, 0)
BLUE_COLOR: str = rgb(0, 255, 255)

TEST_BUTTON_KEY: str = 'dd8fe8f21b59e4d70f144900fbf286a2'
CLOSE_BUTTON_KEY: str = 'e48f38b2f4d895fe81e9604877fee9d9'
LAST_CHECK_TEXT_KEY: str = 'ce2082b1ba08ac910de71e10a8643a78'


def main() -> None:
    def generate_key(left_name: str, right_name: str) -> str:
        return md5(f'{left_name}-{right_name}'.encode()).hexdigest()

    def get_background_color(is_success_status: bool) -> str:
        if is_success_status:
            return GREEN_COLOR

        return RED_COLOR

    def get_last_check_text() -> str:
        return strftime('%Y-%m-%d %H:%M:%S')

        # return '0000-00-00 00:00:01'

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
            layout.append([StatusBar(value_name, key=element_key)])

    layout.append([
        Button('Test', key=TEST_BUTTON_KEY, button_color=BLUE_COLOR),
        Button('Close', key=CLOSE_BUTTON_KEY, button_color=RED_COLOR),
        Text('0000-00-00 00:00:00', key=LAST_CHECK_TEXT_KEY)])

    window: Window = Window('Pinger', layout, resizable=True)
    default_element_background_color: str = theme_element_background_color()

    while True:
        event, _ = window.read()

        if event == WIN_CLOSED or event == CLOSE_BUTTON_KEY:
            break

        if event == TEST_BUTTON_KEY:
            for element_key1 in element_keys:
                window[element_key1].update(background_color=default_element_background_color)

            last_check_text: str = get_last_check_text()
            window[LAST_CHECK_TEXT_KEY].update(value=last_check_text)
            window.refresh()

            for section_name in config.sections():
                for value_name in config[section_name]:
                    address: str = config[section_name][value_name]
                    is_ping_success: bool = ping(address)
                    new_background_color: str = get_background_color(is_ping_success)
                    element_key: str = generate_key(section_name, value_name)
                    window[element_key].update(background_color=new_background_color)
                    window.refresh()

    window.close()


if __name__ == '__main__':
    main()
