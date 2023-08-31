from configparser import ConfigParser
from platform import system
from subprocess import check_output
from re import search, Match


SETTINGS_FILENAME: str = 'settings.ini'

WINDOWS_OS: str = 'Windows'
WINDOWS_PING_PARAM: str = '-n'
OTHER_PING_PARAM: str = '-c'

HOST_UNREACHABLE_PING_PATTERN = 'Destination host unreachable'
LOST_PACKAGE_PING_PATTERN = 'Lost = 1'


def main() -> None:
    config: ConfigParser = ConfigParser()
    config.read(SETTINGS_FILENAME)

    for section_name in config.sections():
        for value_name in config[section_name]:
            address = config[section_name][value_name]
            print(value_name, config[section_name][value_name], ping(address))


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
