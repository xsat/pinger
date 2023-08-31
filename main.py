from configparser import ConfigParser
from platform import system
from subprocess import check_output
from re import search, Match
from hashlib import md5
from PySimpleGUI import theme, rgb, Window, Text, StatusBar, Button, WIN_CLOSED


SETTINGS_FILENAME: str = 'settings.ini'

WINDOWS_OS: str = 'Windows'
WINDOWS_PING_PARAM: str = '-n'
OTHER_PING_PARAM: str = '-c'

HOST_UNREACHABLE_PING_PATTERN = 'Destination host unreachable'
LOST_PACKAGE_PING_PATTERN = 'Lost = 1'


BLACK_COLOR = rgb(0, 0, 0)
RED_COLOR = rgb(255, 0, 0)
GREEN_COLOR = rgb(0, 255, 0)
YELLOW_COLOR = rgb(255, 255, 0)


def main() -> None:
    def generate_key(left_name: str, right_name: str) -> str:
        return md5(f'-{left_name}-{right_name}-'.encode()).hexdigest()

    theme('Dark')

    layout = []

    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        layout.append([Text(section_name)])

        for value_name in config[section_name]:
            layout.append([StatusBar(value_name, key=generate_key(section_name, value_name), enable_events=True)])

            # address = config[section_name][value_name]
            # print(value_name, config[section_name][value_name], ping(address))

    layout.append([
        Button('Test', button_color=YELLOW_COLOR),
        Button('Cancel', button_color=RED_COLOR)])

    window = Window('Window Title', layout)

    while True:
        event, values = window.read()
        if event == WIN_CLOSED or event == 'Cancel':
            break
        if event == 'Test':
            for section_name in config.sections():
                for value_name in config[section_name]:
                    address = config[section_name][value_name]
                    if ping(address):
                        window[generate_key(section_name, value_name)].update(background_color=GREEN_COLOR)
                    else:
                        window[generate_key(section_name, value_name)].update(background_color=RED_COLOR)

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

    if system() == WINDOWS_OS:
        param = WINDOWS_PING_PARAM
    else:
        param = OTHER_PING_PARAM

    command: list[str] = ['ping', param, '1', hostname]
    command_result: str = str(check_output(command))

    return (not is_matched(HOST_UNREACHABLE_PING_PATTERN, command_result)
            and not is_matched(LOST_PACKAGE_PING_PATTERN, command_result))


if __name__ == '__main__':
    main()
