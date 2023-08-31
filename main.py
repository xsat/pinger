from configparser import ConfigParser
from platform import system
from subprocess import check_output, CalledProcessError
from re import search, Match
from hashlib import md5
from PySimpleGUI import theme, rgb, theme_element_background_color, Window, Text, StatusBar, Button, WIN_CLOSED


SETTINGS_FILENAME: str = 'settings.ini'

WINDOWS_OS: str = 'Windows'
WINDOWS_PING_PARAM: str = '-n'
OTHER_PING_PARAM: str = '-c'

HOST_UNREACHABLE_PING_PATTERN: str = 'Destination host unreachable'
LOST_PACKAGE_PING_PATTERN: str = 'Lost = 1'


BLACK_COLOR: str = rgb(0, 0, 0)
RED_COLOR: str = rgb(255, 0, 0)
GREEN_COLOR: str = rgb(0, 255, 0)
YELLOW_COLOR: str = rgb(255, 255, 0)


TEST_BUTTON_KEY: str = 'dd8fe8f21b59e4d70f144900fbf286a2'
CLOSE_BUTTON_KEY: str = 'e48f38b2f4d895fe81e9604877fee9d9'


def main() -> None:
    def generate_key(left_name: str, right_name: str) -> str:
        return md5(f'{left_name}-{right_name}'.encode()).hexdigest()

    def get_background_color(is_success_status: bool) -> str:
        if is_success_status:
            return GREEN_COLOR

        return RED_COLOR

    theme('Dark')

    default_element_background_color: str = theme_element_background_color()

    layout = []
    element_keys = []

    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        layout.append([Text(section_name)])

        for value_name in config[section_name]:
            element_key = generate_key(section_name, value_name)
            element_keys.append(element_key)
            layout.append([StatusBar(value_name, key=element_key)])

    layout.append([
        Button('Test', key=TEST_BUTTON_KEY, button_color=YELLOW_COLOR),
        Button('Close', key=CLOSE_BUTTON_KEY, button_color=RED_COLOR)])

    window: Window = Window('Window Title', layout)

    while True:
        event, values = window.read()

        if event == WIN_CLOSED or event == CLOSE_BUTTON_KEY:
            break

        if event == TEST_BUTTON_KEY:
            for element_key1 in element_keys:
                window[element_key1].update(background_color=default_element_background_color)

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

    # config: ConfigParser = ConfigParser()
    # config.read(SETTINGS_FILENAME)
    #
    # for section_name in config.sections():
    #     for value_name in config[section_name]:
    #         address = config[section_name][value_name]
    #         print(value_name, config[section_name][value_name], ping(address))


def ping(hostname: str) -> bool:
    def is_matched(pattern: str, string: str) -> bool:
        search_result: Match[str] = search(pattern, string)

        return search_result is not None

    def get_ping_param() -> str:
        if system() == WINDOWS_OS:
            return WINDOWS_PING_PARAM

        return OTHER_PING_PARAM

    param: str = get_ping_param()
    command: list[str] = ['ping', param, '1', hostname]

    try:
        command_result: str = str(check_output(command))

        return (not is_matched(HOST_UNREACHABLE_PING_PATTERN, command_result)
                and not is_matched(LOST_PACKAGE_PING_PATTERN, command_result))
    except CalledProcessError:
        return False


if __name__ == '__main__':
    main()
